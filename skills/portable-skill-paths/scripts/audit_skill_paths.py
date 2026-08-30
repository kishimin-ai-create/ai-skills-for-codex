"""Audit Skill markdown for paths that may not transfer between computers."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PATH_PATTERN = re.compile(
    r"(?:[A-Za-z]:[\\/][^\s`'\"]+|/(?:Users|home|workspace|workspaces)/[^\s`'\"]+|\$(?:HOME|CODEX_HOME)(?:[/\\][^\s`'\"]+)?)"
)
def classify(reference: str) -> str:
    if reference.startswith("$HOME") or reference.startswith("$CODEX_HOME"):
        return "canonical"
    if reference.startswith(("/Users/", "/home/")) or re.match(r"^[A-Za-z]:[\\/]", reference):
        return "machine-specific"
    return "review"


def redact(reference: str) -> str:
    if reference.startswith("$HOME"):
        return reference.replace("$HOME", "<HOME>", 1)
    if reference.startswith("$CODEX_HOME"):
        return reference.replace("$CODEX_HOME", "<CODEX_HOME>", 1)
    return "<PROJECT_ROOT>"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skills_root", type=Path)
    parser.add_argument("--redact", action="store_true", help="redact references in the report")
    args = parser.parse_args()

    root = args.skills_root.resolve()
    files = sorted(root.rglob("SKILL.md"))
    display_root = "<SKILLS_ROOT>" if args.redact else str(root)
    print(f"# Skill path audit: `{display_root}`")
    print(f"\nScanned Skill files: {len(files)}")
    print("\n| Skill | Line | Reference | Classification |")
    print("| --- | ---: | --- | --- |")

    findings = 0
    for file in files:
        for line_number, line in enumerate(file.read_text(encoding="utf-8").splitlines(), 1):
            for match in PATH_PATTERN.finditer(line):
                reference = match.group(0)
                shown = redact(reference) if args.redact else reference
                relative = file.relative_to(root).as_posix()
                print(f"| `{relative}` | {line_number} | `{shown}` | {classify(reference)} |")
                findings += 1

    if not findings:
        print("| (none) |  |  |  |")
    print(f"\nFindings: {findings}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
