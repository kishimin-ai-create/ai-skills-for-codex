---
name: work-session-log
description: "Record resumable development work, including exact user prompts, decisions, verification, and next actions, in repository work logs."
---

# Work Session Log

Use this skill for development work that may cross assistant sessions, calendar days, branches, or interruptions. The log is evidence for deciding whether repeated work deserves a dedicated skill or an AI configuration change.

## Location and naming

- Store logs under the upper project's `work-logs/` directory, outside child repository `docs/` directories.
- Prefer one file per child project and branch or work item: `<project>-<branch-or-task>.md`.
- Use a stable filename so a later session can append to the same log.
- Do not embed machine-specific absolute paths in reusable instructions or shared logs. Use placeholders such as `<PROJECT_ROOT>`, `<REPO_ROOT>`, `<WORK_LOG_ROOT>`, `<BRANCH>`, and `<DATE>`.
- Derive filenames from placeholders (for example, `<PROJECT>-<BRANCH_SLUG>.md`); replace `/` in branch names with `-` when creating a filename.
- On another PC, update only the local path mapping or placeholder values; do not rewrite the workflow itself.

## Portability and redaction

At the top of a log, keep a local-only mapping when an exact path is needed:

```md
## Local path mapping
- `<PROJECT_ROOT>`: <local project path>
- `<REPO_ROOT>`: <local repository path>
- `<WORK_LOG_ROOT>`: <local log path>
```

Before sharing or committing a log, apply blur/redaction to machine-specific or identifying values:

- user names and home directories → `[REDACTED_USER]`
- host names, drive letters, and absolute paths → `[REDACTED_HOST]` / `<PROJECT_ROOT>`
- tokens, credentials, private URLs, and personal identifiers → `[REDACTED_SECRET]` or `[REDACTED_PERSONAL]`
- retain relative paths, filenames, branch names, dates, and command names when they are needed to reproduce the work

Record that redaction was applied and which category was replaced. Keep the unredacted value out of repository artifacts. Prompt history remains verbatim unless it contains one of these sensitive values; in that case redact only the sensitive value and note the reason.

## Required log contents

Maintain these sections and append entries chronologically:

```md
# Work log: <work item>

## Purpose
- Why this work is being tracked:

## Prompt history
### <ISO timestamp>
```text
<exact user prompt>
```

## Decisions
- <decision and evidence>

## Progress
- Completed:
- In progress:
- Blocked:

## Verification
- `<command>`: <result>

## Resume checkpoint
- Next action:
- Target files:
- Expected result:

## Skill/configuration assessment
- Repeated pattern:
- Frequency evidence:
- Candidate skill or AI setting:
- Decision: keep manual / template / skill / configuration change
```

Record every user instruction that changes scope, acceptance criteria, implementation, or priority in `Prompt history` verbatim. Preserve the original language and line breaks where practical. If a prompt contains a secret or personal credential, redact only the sensitive value and record that redaction occurred; never write secrets to the repository.

Record assistant decisions only when they affect the work. Separate facts (commands and results), assumptions, decisions, and unresolved questions. Update `Resume checkpoint` before ending a session or changing tasks. On resumption, read the existing log before inspecting unrelated files and continue from the checkpoint.

When work is complete, update the log before reporting completion. Record the completed scope, verification results, skipped or failed checks with reasons, remaining risks, and the highest-priority next action. Do not report completion until this entry exists.

## Evaluation guidance

Do not create a skill merely because one task was documented. After several entries, evaluate frequency, procedural stability, repeated inputs/outputs, judgment required, error cost, and the quality of cross-session recovery. A stable repeated procedure supports a skill; variable judgment supports a checklist or reference; repeated configuration friction supports an AI configuration change.

Do not log generated artifacts, secrets, or unrelated conversation. Do not replace the repository's implementation plan, ADR, diary, or review documents; link to them from the work log when relevant.
