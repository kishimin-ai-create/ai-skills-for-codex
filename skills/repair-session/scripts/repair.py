"""Extract agent-session evidence and prepare reversible instruction repairs."""

from contextlib import ExitStack, contextmanager
import argparse
import codecs
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
import uuid


SESSION_ID = re.compile(
    r"(?i)\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"
)
REPO = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path, data, mode=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if mode is not None:
            os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def save(path, value):
    write(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode())


def plain_path(path):
    path = path.absolute()
    for part in (path, *path.parents):
        is_reparse_point = (
            part.exists()
            and getattr(part.lstat(), "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        )
        require(not part.is_symlink() and not is_reparse_point, "Links are not repair targets")
    return path.resolve()


def private(path):
    path = plain_path(path.expanduser())
    require(not path.is_relative_to(REPO), "Keep case data outside this skill")
    return path


@contextmanager
def lock(path):
    directory = Path(tempfile.gettempdir()) / "agent-repair-locks"
    directory.mkdir(exist_ok=True)
    key = hashlib.sha256(os.path.normcase(str(path.resolve())).encode()).hexdigest()
    with (directory / key).open("a+b") as handle:
        handle.seek(0, 2)
        if not handle.tell():
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            if os.name == "nt":
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def load_records(path):
    records = []
    gaps = []
    with path.open(encoding="utf-8-sig") as stream:
        for line, raw in enumerate(stream, 1):
            if not raw.strip():
                continue
            try:
                record = json.loads(raw)
                require(isinstance(record, dict), "Expected a JSON object")
                records.append((line, record))
            except (json.JSONDecodeError, ValueError):
                gaps.append({"line": line, "reason": "malformed_record"})
    require(records, "No supported session records found")
    return records, gaps


def identify_tool(records):
    if any(record.get("type") in {"session_meta", "response_item"} for _, record in records):
        return "codex"
    if any(
        record.get("type") in {"user", "assistant"} and "sessionId" in record
        for _, record in records
    ):
        return "claude"
    raise ValueError("Session format is not recognized as Codex or Claude Code")


def find_session(value, codex_home, claude_home):
    supplied = Path(value).expanduser()
    if supplied.is_file():
        records, gaps = load_records(supplied.resolve())
        return supplied.resolve(), identify_tool(records), records, gaps

    identifiers = set(SESSION_ID.findall(value))
    require(len(identifiers) == 1, "Supply one session UUID or a local JSONL file")
    identifier = next(iter(identifiers)).lower()
    candidates = []
    for folder in (codex_home / "sessions", codex_home / "archived_sessions"):
        if folder.is_dir():
            candidates.extend((path, "codex") for path in folder.rglob(f"*{identifier}*.jsonl"))
    claude_projects = claude_home / "projects"
    if claude_projects.is_dir():
        candidates.extend(
            (path, "claude") for path in claude_projects.rglob(f"*{identifier}*.jsonl")
        )
    unique = {(path.resolve(), tool) for path, tool in candidates}
    require(len(unique) == 1, "Session not found uniquely; supply its JSONL path")
    source, expected_tool = unique.pop()
    records, gaps = load_records(source)
    actual_tool = identify_tool(records)
    require(actual_tool == expected_tool, "Session location and content disagree")
    return source, actual_tool, records, gaps


def codex_content_text(content):
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    return "\n".join(
        item.get("text", "")
        for item in content
        if isinstance(item, dict) and isinstance(item.get("text"), str)
    )


def parse_codex(records, gaps):
    metadata = {}
    events = []
    fallback = []
    for line, record in records:
        kind = record.get("type")
        payload = record.get("payload", {})
        if not isinstance(payload, dict):
            gaps.append({"line": line, "reason": "invalid_payload"})
            continue
        if kind in {"session_meta", "turn_context"}:
            metadata.update(
                {key: payload[key] for key in ("id", "cwd", "automation_id") if key in payload}
            )
        elif kind in {"compacted", "context_compacted"}:
            gaps.append({"line": line, "reason": "compaction"})
        elif kind == "response_item":
            event_type = payload.get("type")
            if event_type == "message" and payload.get("role") in {"user", "assistant"}:
                events.append(
                    {
                        "line": line,
                        "kind": payload["role"],
                        "text": codex_content_text(payload.get("content", [])),
                    }
                )
            elif event_type in {
                "function_call",
                "custom_tool_call",
                "function_call_output",
                "custom_tool_call_output",
            }:
                events.append(
                    {
                        "line": line,
                        "kind": event_type,
                        **{
                            key: payload[key]
                            for key in ("name", "call_id", "arguments", "input", "output")
                            if key in payload
                        },
                    }
                )
        elif kind == "event_msg" and payload.get("type") in {
            "user_message",
            "agent_message",
        }:
            fallback.append(
                {
                    "line": line,
                    "kind": payload["type"],
                    "text": payload.get("message", ""),
                }
            )
    require(events or fallback, "No supported conversation events found")
    return {"metadata": metadata, "gaps": gaps, "events": events or fallback}


def parse_claude(records, gaps):
    metadata = {}
    events = []
    for line, record in records:
        record_type = record.get("type")
        if record_type not in {"user", "assistant"}:
            continue
        metadata.update(
            {
                key: record[key]
                for key in ("sessionId", "cwd", "gitBranch")
                if key in record
            }
        )
        message = record.get("message")
        if not isinstance(message, dict):
            gaps.append({"line": line, "reason": "invalid_message"})
            continue
        role = message.get("role")
        content = message.get("content", "")
        if isinstance(content, str):
            if role in {"user", "assistant"}:
                events.append({"line": line, "kind": role, "text": content})
            continue
        if not isinstance(content, list):
            gaps.append({"line": line, "reason": "invalid_content"})
            continue
        text_parts = [
            item["text"]
            for item in content
            if isinstance(item, dict)
            and item.get("type") == "text"
            and isinstance(item.get("text"), str)
        ]
        if text_parts and role in {"user", "assistant"}:
            events.append(
                {"line": line, "kind": role, "text": "\n".join(text_parts)}
            )
        for item in content:
            if not isinstance(item, dict):
                continue
            item_type = item.get("type")
            if item_type == "tool_use":
                events.append(
                    {
                        "line": line,
                        "kind": "tool_use",
                        **{
                            key: item[key]
                            for key in ("id", "name", "input")
                            if key in item
                        },
                    }
                )
            elif item_type == "tool_result":
                events.append(
                    {
                        "line": line,
                        "kind": "tool_result",
                        **{
                            key: item[key]
                            for key in ("tool_use_id", "content", "is_error")
                            if key in item
                        },
                    }
                )
    require(events, "No supported conversation events found")
    return {"metadata": metadata, "gaps": gaps, "events": events}


def inspect_session(value, codex_home, claude_home, state=None):
    codex_home = Path(codex_home).expanduser().resolve()
    claude_home = Path(claude_home).expanduser().resolve()
    source, tool, records, gaps = find_session(value, codex_home, claude_home)
    evidence = (
        parse_codex(records, gaps)
        if tool == "codex"
        else parse_claude(records, gaps)
    )
    evidence["source"] = str(source)
    evidence["tool"] = tool
    default_home = codex_home if tool == "codex" else claude_home
    case_root = private(Path(state)) if state else private(default_home / "agent-repair")
    case = case_root / uuid.uuid4().hex
    save(case / "session.json", evidence)
    save(case / "case.json", {"status": "inspected", "tool": tool, "files": []})
    return {
        "case": str(case),
        "session": str(case / "session.json"),
        "tool": tool,
        "events": len(evidence["events"]),
        "gaps": gaps,
    }


def stage(case, sources, plan):
    case = private(Path(case))
    require(read(case / "case.json")["status"] == "inspected", "Start a new case before staging files")
    checks = read(Path(plan))
    require(isinstance(checks, list) and checks, "Plan must be a list of checks")
    require(
        {check["kind"] for check in checks} == {"source", "similar", "regression"},
        "Plan needs source, similar and regression checks",
    )
    require(
        len({check["name"] for check in checks}) == len(checks)
        and all(check["name"] and check["check"] for check in checks),
        "Checks need unique names and descriptions",
    )
    sources = [plain_path(Path(source).expanduser()) for source in sources]
    require(sources, "Supply at least one file")
    bases = {
        source.anchor: Path(
            os.path.commonpath(
                [str(item.parent) for item in sources if item.anchor == source.anchor]
            )
        )
        for source in sources
    }
    groups = {anchor: f"{index:02d}" for index, anchor in enumerate(sorted(bases))}
    files = []
    seen = set()
    for source in sources:
        require(source.is_file() and source not in seen, "Supply distinct existing files")
        require(not source.is_relative_to(case), "A case copy cannot be a source")
        require(
            not any(
                part.startswith(".env")
                or part in {".git", "auth.json", "credentials.json", ".credentials.json"}
                for part in source.parts
            )
            and source.suffix.lower() not in {".pem", ".key"},
            "Do not stage credential or Git files",
        )
        seen.add(source)
        raw = source.read_bytes()
        require(len(raw) <= 500_000 and b"\0" not in raw, "Only small UTF-8 text files are supported")
        raw.decode("utf-8-sig")
        name = groups[source.anchor] + "/" + source.relative_to(bases[source.anchor]).as_posix()
        for version in ("original", "candidate"):
            write(case / version / name, raw)
        files.append(
            {
                "source": str(source),
                "name": name,
                "before": sha(source),
                "mode": stat.S_IMODE(source.stat().st_mode),
            }
        )
    save(case / "plan.json", checks)
    manifest = {
        "status": "staged",
        "tool": read(case / "case.json")["tool"],
        "files": files,
        "plan_sha256": sha(case / "plan.json"),
    }
    save(case / "case.json", manifest)
    return manifest


def copy_file(case, version, entry):
    root = (case / version).resolve()
    path = plain_path(root / entry["name"])
    require(path.is_relative_to(root), "Copy path escapes the case")
    return path


def seal(case):
    case = private(Path(case))
    manifest = read(case / "case.json")
    require(manifest["status"] in {"staged", "sealed"}, "Case cannot be sealed")
    require(sha(case / "plan.json") == manifest["plan_sha256"], "Test plan changed")
    patch = []
    for entry in manifest["files"]:
        original = copy_file(case, "original", entry)
        candidate = copy_file(case, "candidate", entry)
        require(sha(original) == entry["before"], "Original copy changed")
        raw = candidate.read_bytes()
        text = raw.decode("utf-8-sig")
        require(len(raw) <= 650_000 and "\0" not in text, "Invalid candidate text")
        if original.read_bytes().startswith(codecs.BOM_UTF8) and not raw.startswith(codecs.BOM_UTF8):
            write(candidate, codecs.BOM_UTF8 + raw)
            raw = candidate.read_bytes()
        if candidate.suffix == ".py":
            compile(text, str(candidate), "exec")
        entry["after"] = sha(candidate)
        patch.extend(
            difflib.unified_diff(
                original.read_text(encoding="utf-8-sig").splitlines(True),
                candidate.read_text(encoding="utf-8-sig").splitlines(True),
                fromfile="original/" + entry["name"],
                tofile="candidate/" + entry["name"],
            )
        )
    require(any(entry["before"] != entry["after"] for entry in manifest["files"]), "No file changes")
    write(case / "changes.patch", "".join(patch).encode())
    manifest["status"] = "sealed"
    manifest["revision"] = uuid.uuid4().hex
    save(case / "case.json", manifest)
    return {"revision": manifest["revision"], "diff": str(case / "changes.patch")}


def validate_results(case, manifest, results):
    require(
        results.get("revision") == manifest["revision"] and results.get("reviewed") is True,
        "Results must review this sealed revision",
    )
    require(sha(case / "plan.json") == manifest["plan_sha256"], "Test plan changed")
    plan = {check["name"]: check for check in read(case / "plan.json")}
    checks = results.get("checks", [])
    require(
        len(checks) == len(plan) and {check["name"] for check in checks} == plan.keys(),
        "Results must cover every planned check",
    )
    improved = False
    for check in checks:
        before = check["before"]
        after = check["after"]
        require(
            isinstance(before, list)
            and isinstance(after, list)
            and before
            and len(before) == len(after)
            and all(type(value) is bool for value in before + after),
            "Use equally sized lists of boolean trial results",
        )
        require(
            isinstance(check.get("evidence"), str) and check["evidence"].strip(),
            "Record observed evidence for each check",
        )
        require(sum(after) >= sum(before), "A planned check regressed")
        if plan[check["name"]]["kind"] == "source":
            require(all(after), "The original failure remains")
            improved |= sum(after) > sum(before)
    require(improved, "No demonstrated improvement on the original failure")


def purge_directory(path):
    if not path.exists():
        return
    require(path.is_dir() and not path.is_symlink(), "Sensitive-data directory is invalid")
    descendants = sorted(path.rglob("*"), key=lambda item: len(item.parts), reverse=True)
    for descendant in descendants:
        require(not descendant.is_symlink(), "Sensitive-data directory contains a link")
        descendant.rmdir() if descendant.is_dir() else descendant.unlink()
    path.rmdir()


def purge_sensitive(case):
    session = case / "session.json"
    if session.exists():
        require(session.is_file() and not session.is_symlink(), "Session evidence path is invalid")
        session.unlink()
    purge_directory(case / "samples")


def complete_external(case, approved_case=None):
    case = private(Path(case))
    manifest = read(case / "case.json")
    require(manifest["status"] == "inspected", "External completion needs an inspected case")
    require(
        approved_case is not None and approved_case == case.name,
        "Explicit approval must name the case",
    )
    purge_sensitive(case)
    manifest["status"] = "external_applied"
    save(case / "case.json", manifest)
    return manifest


def rollback_locked(case, manifest):
    conflicts = []
    for entry in reversed(manifest["files"]):
        try:
            source = plain_path(Path(entry["source"]))
            if sha(source) == entry["before"]:
                continue
            require(sha(source) == entry["after"], "Source was edited later")
            backup = copy_file(case, "original", entry)
            require(sha(backup) == entry["before"], "Backup changed")
            write(source, backup.read_bytes(), entry["mode"])
        except (OSError, ValueError) as error:
            conflicts.append({"file": entry["source"], "error": str(error)})
    manifest.update(status="rollback_conflict" if conflicts else "rolled_back", conflicts=conflicts)
    save(case / "case.json", manifest)
    return manifest


def update_files(case, results=None, approved_revision=None, rollback=False):
    case = private(Path(case))
    with ExitStack() as stack:
        stack.enter_context(lock(case))
        manifest = read(case / "case.json")
        for source in sorted({entry["source"] for entry in manifest["files"]}):
            stack.enter_context(lock(Path(source)))
        if rollback:
            require(
                manifest["status"] in {"applying", "applied", "rollback_conflict", "rolled_back"},
                "This case has not written files",
            )
            return rollback_locked(case, manifest)
        require(manifest["status"] == "sealed", "Seal and test the candidate before applying")
        require(
            approved_revision is not None and approved_revision == manifest["revision"],
            "Explicit approval must name the sealed revision",
        )
        validate_results(case, manifest, results)
        for entry in manifest["files"]:
            require(sha(plain_path(Path(entry["source"]))) == entry["before"], "Source changed after staging")
            require(sha(copy_file(case, "original", entry)) == entry["before"], "Backup changed")
            require(sha(copy_file(case, "candidate", entry)) == entry["after"], "Candidate changed after sealing")
        save(case / "results.json", results)
        manifest["status"] = "applying"
        save(case / "case.json", manifest)
        try:
            for entry in manifest["files"]:
                if entry["before"] == entry["after"]:
                    continue
                source = plain_path(Path(entry["source"]))
                candidate = copy_file(case, "candidate", entry)
                require(sha(source) == entry["before"] and sha(candidate) == entry["after"], "Files changed during application")
                write(source, candidate.read_bytes(), entry["mode"])
            require(
                all(sha(Path(entry["source"])) == entry["after"] for entry in manifest["files"]),
                "Applied files do not match the tested revision",
            )
            purge_sensitive(case)
        except Exception:
            rollback_locked(case, manifest)
            raise
        manifest["status"] = "applied"
        save(case / "case.json", manifest)
        return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    claude_home = Path(os.environ.get("CLAUDE_HOME", Path.home() / ".claude"))

    inspect = commands.add_parser("inspect")
    inspect.add_argument("session")
    inspect.add_argument("--codex-home", type=Path, default=codex_home)
    inspect.add_argument("--claude-home", type=Path, default=claude_home)
    inspect.add_argument("--state", type=Path)

    stage_command = commands.add_parser("stage")
    stage_command.add_argument("case", type=Path)
    stage_command.add_argument("files", nargs="+", type=Path)
    stage_command.add_argument("--plan", required=True, type=Path)

    seal_command = commands.add_parser("seal")
    seal_command.add_argument("case", type=Path)

    apply_command = commands.add_parser("apply")
    apply_command.add_argument("case", type=Path)
    apply_command.add_argument("--results", required=True, type=Path)
    apply_command.add_argument("--approved-revision", required=True)

    rollback_command = commands.add_parser("rollback")
    rollback_command.add_argument("case", type=Path)

    complete_command = commands.add_parser("complete-external")
    complete_command.add_argument("case", type=Path)
    complete_command.add_argument("--approved-case", required=True)

    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            result = inspect_session(
                args.session,
                args.codex_home,
                args.claude_home,
                args.state,
            )
        elif args.command == "stage":
            result = stage(args.case, args.files, args.plan)
        elif args.command == "seal":
            result = seal(args.case)
        elif args.command == "apply":
            result = update_files(
                args.case,
                read(args.results),
                approved_revision=args.approved_revision,
            )
        elif args.command == "rollback":
            result = update_files(args.case, rollback=True)
        else:
            result = complete_external(args.case, args.approved_case)
        print(json.dumps(result, ensure_ascii=False))
        return int(result.get("status") == "rollback_conflict")
    except (OSError, ValueError, KeyError, TypeError, SyntaxError) as error:
        print(f"Error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
