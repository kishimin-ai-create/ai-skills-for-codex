import importlib.util
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "repair.py"
SPEC = importlib.util.spec_from_file_location("repair", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load repair module")
repair = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(repair)


class RepairTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.codex_home = self.root / ".codex"
        self.claude_home = self.root / ".claude"
        self.codex_home.mkdir()
        self.claude_home.mkdir()

    def write_jsonl(self, path, records):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "\n".join(json.dumps(record) for record in records) + "\n",
            encoding="utf-8",
        )

    def test_inspect_codex_session_uses_codex_state_and_excludes_reasoning(self):
        session_id = "00000000-0000-0000-0000-000000000001"
        trace = self.codex_home / "sessions" / f"rollout-{session_id}.jsonl"
        self.write_jsonl(
            trace,
            [
                {"type": "session_meta", "payload": {"id": session_id, "cwd": "C:/repo"}},
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": "Fix the failure."}],
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "reasoning",
                        "encrypted_content": "private-reasoning",
                    },
                },
            ],
        )

        result = repair.inspect_session(session_id, self.codex_home, self.claude_home)

        case = Path(result["case"])
        session = json.loads((case / "session.json").read_text(encoding="utf-8"))
        self.assertEqual(result["tool"], "codex")
        self.assertEqual(case.parent, self.codex_home / "agent-repair")
        self.assertEqual(session["events"][0]["text"], "Fix the failure.")
        self.assertNotIn("private-reasoning", json.dumps(session))

    def test_inspect_claude_session_uses_claude_state_and_excludes_thinking(self):
        session_id = "00000000-0000-0000-0000-000000000002"
        trace = self.claude_home / "projects" / "project" / f"{session_id}.jsonl"
        self.write_jsonl(
            trace,
            [
                {
                    "type": "user",
                    "sessionId": session_id,
                    "cwd": "C:/repo",
                    "message": {"role": "user", "content": "Repair this session."},
                },
                {
                    "type": "assistant",
                    "sessionId": session_id,
                    "cwd": "C:/repo",
                    "message": {
                        "role": "assistant",
                        "content": [
                            {"type": "thinking", "thinking": "private-thought"},
                            {"type": "text", "text": "I will inspect it."},
                            {
                                "type": "tool_use",
                                "id": "tool-1",
                                "name": "Read",
                                "input": {"file_path": "SKILL.md"},
                            },
                        ],
                    },
                },
                {
                    "type": "user",
                    "sessionId": session_id,
                    "message": {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": "tool-1",
                                "content": "skill contents",
                            }
                        ],
                    },
                },
            ],
        )

        result = repair.inspect_session(session_id, self.codex_home, self.claude_home)

        case = Path(result["case"])
        session = json.loads((case / "session.json").read_text(encoding="utf-8"))
        self.assertEqual(result["tool"], "claude")
        self.assertEqual(case.parent, self.claude_home / "agent-repair")
        self.assertEqual([event["kind"] for event in session["events"]], [
            "user",
            "assistant",
            "tool_use",
            "tool_result",
        ])
        self.assertNotIn("private-thought", json.dumps(session))

    def test_apply_requires_revision_approval_purges_session_and_can_rollback(self):
        session_id = "00000000-0000-0000-0000-000000000003"
        trace = self.codex_home / "sessions" / f"rollout-{session_id}.jsonl"
        self.write_jsonl(
            trace,
            [
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [{"text": "Repair the skill."}],
                    },
                }
            ],
        )
        case = Path(
            repair.inspect_session(session_id, self.codex_home, self.claude_home)[
                "case"
            ]
        )
        source = self.root / "skill" / "SKILL.md"
        source.parent.mkdir()
        source.write_text("Read the first record.\n", encoding="utf-8")
        plan = self.root / "plan.json"
        repair.save(
            plan,
            [
                {"name": kind, "kind": kind, "check": "Observe expected behavior."}
                for kind in ("source", "similar", "regression")
            ],
        )
        manifest = repair.stage(case, [source], plan)
        candidate = case / "candidate" / manifest["files"][0]["name"]
        candidate.write_text("Read every record.\n", encoding="utf-8")
        sample = case / "samples" / "trial.json"
        repair.save(sample, {"output": "sensitive sample"})
        revision = repair.seal(case)["revision"]
        results = {
            "revision": revision,
            "reviewed": True,
            "checks": [
                {
                    "name": kind,
                    "before": [kind == "regression"],
                    "after": [True],
                    "evidence": "Observed in an isolated fixture.",
                }
                for kind in ("source", "similar", "regression")
            ],
        }

        with self.assertRaisesRegex(ValueError, "approval"):
            repair.update_files(case, results)
        self.assertEqual(source.read_text(encoding="utf-8"), "Read the first record.\n")

        applied = repair.update_files(case, results, approved_revision=revision)

        self.assertEqual(applied["status"], "applied")
        self.assertEqual(source.read_text(encoding="utf-8"), "Read every record.\n")
        self.assertFalse((case / "session.json").exists())
        self.assertFalse((case / "samples").exists())
        self.assertTrue((case / "results.json").exists())
        self.assertEqual(repair.update_files(case, rollback=True)["status"], "rolled_back")
        self.assertEqual(source.read_text(encoding="utf-8"), "Read the first record.\n")

    def test_cli_inspect_accepts_both_agent_home_paths(self):
        session_id = "00000000-0000-0000-0000-000000000004"
        trace = self.claude_home / "projects" / "project" / f"{session_id}.jsonl"
        self.write_jsonl(
            trace,
            [
                {
                    "type": "user",
                    "sessionId": session_id,
                    "message": {"role": "user", "content": "Repair this session."},
                }
            ],
        )

        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = repair.main(
                [
                    "inspect",
                    session_id,
                    "--codex-home",
                    str(self.codex_home),
                    "--claude-home",
                    str(self.claude_home),
                ]
            )

        result = json.loads(output.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(result["tool"], "claude")

    def test_repair_rejects_credentials_path_escape_and_changed_sources(self):
        session_id = "00000000-0000-0000-0000-000000000005"
        trace = self.codex_home / "sessions" / f"rollout-{session_id}.jsonl"
        self.write_jsonl(
            trace,
            [
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [{"text": "Repair the skill."}],
                    },
                }
            ],
        )
        case = Path(
            repair.inspect_session(session_id, self.codex_home, self.claude_home)[
                "case"
            ]
        )
        plan = self.root / "plan.json"
        repair.save(
            plan,
            [
                {"name": kind, "kind": kind, "check": "Observe expected behavior."}
                for kind in ("source", "similar", "regression")
            ],
        )
        credential = self.root / ".credentials.json"
        credential.write_text('{"token":"secret"}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "credential"):
            repair.stage(case, [credential], plan)

        source = self.root / "skill" / "SKILL.md"
        source.parent.mkdir()
        source.write_text("Before\n", encoding="utf-8")
        manifest = repair.stage(case, [source], plan)
        candidate = case / "candidate" / manifest["files"][0]["name"]
        candidate.write_text("After\n", encoding="utf-8")
        revision = repair.seal(case)["revision"]
        results = {
            "revision": revision,
            "reviewed": True,
            "checks": [
                {
                    "name": kind,
                    "before": [kind == "regression"],
                    "after": [True],
                    "evidence": "Observed in an isolated fixture.",
                }
                for kind in ("source", "similar", "regression")
            ],
        }
        source.write_text("Intervening edit\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Source changed"):
            repair.update_files(case, results, approved_revision=revision)
        with self.assertRaisesRegex(ValueError, "escapes"):
            repair.copy_file(case, "candidate", {"name": "../../outside.txt"})

    def test_external_prompt_completion_requires_case_approval_and_purges_evidence(self):
        session_id = "00000000-0000-0000-0000-000000000006"
        trace = self.codex_home / "sessions" / f"rollout-{session_id}.jsonl"
        self.write_jsonl(
            trace,
            [
                {
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [{"text": "Repair the automation prompt."}],
                    },
                }
            ],
        )
        case = Path(
            repair.inspect_session(session_id, self.codex_home, self.claude_home)[
                "case"
            ]
        )
        repair.save(case / "samples" / "trial.json", {"output": "sensitive sample"})

        with self.assertRaisesRegex(ValueError, "approval"):
            repair.complete_external(case)

        completed = repair.complete_external(case, approved_case=case.name)

        self.assertEqual(completed["status"], "external_applied")
        self.assertFalse((case / "session.json").exists())
        self.assertFalse((case / "samples").exists())


if __name__ == "__main__":
    unittest.main()
