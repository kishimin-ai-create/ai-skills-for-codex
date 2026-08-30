---
name: portable-skill-paths
description: "Audit and parameterize Skill input/output paths for reuse across computers, with safe redaction of machine-specific values."
---

# Portable Skill Paths

Use this skill when a Skill contains file names, input paths, output paths, or machine-specific references that must work on another computer. Audit first; do not rewrite every Skill automatically.

## Workflow

1. Run `scripts/audit_skill_paths.py <skills-root>` and inspect the report.
2. Classify each reference as canonical (`$HOME`, `$CODEX_HOME`), project-relative, machine-specific, generated, or uncertain.
3. Replace only machine-specific and reusable project-specific references with placeholders. Preserve canonical configuration paths and examples whose meaning is not a filesystem path.
4. Use placeholders consistently: `<HOME>`, `<CODEX_HOME>`, `<AGENTS_SKILLS_ROOT>`, `<PROJECT_ROOT>`, `<REPO_ROOT>`, `<WORK_LOG_ROOT>`, `<BRANCH_SLUG>`, and `<DATE>`.
5. Make filenames parameterized (for example, `<PROJECT>-<BRANCH_SLUG>.md`) and document how `/` is converted to `-`.
6. Run the audit again and review the diff. The default operation is read-only; editing requires an explicit target Skill and a reviewed diff.

## Redaction

When preparing a report or shared copy, use the script's redaction mode or apply the same categories manually:

- user names and home directories → `[REDACTED_USER]` / `<HOME>`
- drive letters, host names, and absolute machine paths → `[REDACTED_HOST]` / `<PROJECT_ROOT>`
- credentials, tokens, private URLs, and personal identifiers → `[REDACTED_SECRET]` / `[REDACTED_PERSONAL]`

Redaction applies to reports and shared copies, never to the operational path used to execute a command. Record which categories were redacted. Never commit the unredacted value.

## Output contract

Report the scanned root, Skill files inspected, references classified, files changed (if any), redactions, verification command and result, unresolved references, and the next recommended audit action. Do not claim all Skills are portable until the report covers the complete requested root.
