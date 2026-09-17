import importlib.util
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


if __name__ == "__main__":
    unittest.main()
