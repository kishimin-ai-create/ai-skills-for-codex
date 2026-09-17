"""Extract agent-session evidence and prepare reversible instruction repairs."""

import json
import os
from pathlib import Path
import re
import tempfile
import uuid


SESSION_ID = re.compile(
    r"(?i)\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def save(path, value):
    write(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode())


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
    case_root = Path(state).expanduser().resolve() if state else default_home / "agent-repair"
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
