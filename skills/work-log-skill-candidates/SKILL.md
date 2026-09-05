---
name: work-log-skill-candidates
description: "Analyze work logs to decide whether recurring tasks should become a Skill, checklist, AI configuration change, or remain manual."
---

# Work Log Skill Candidates

Use this skill when work logs contain repeated tasks and you need evidence-based guidance about automation or Skill creation. It analyzes logs; it does not create or modify another Skill unless the user explicitly requests that follow-up.

## Workflow

1. Resolve the work-log root from the user-provided path. If none is provided, use `<WORK_LOG_ROOT>` from the current project instructions; do not guess a machine-specific path.
2. Read all relevant log files and extract prompt history, decisions, progress, verification, and skill/configuration assessments. Preserve exact prompts only in evidence notes; do not copy secrets or personal identifiers into the report.
3. Group tasks by observable outcome and repeated input/output, not by superficial wording. Separate one-off incidents from recurring procedures.
4. Evaluate each group with the rubric in [candidate-rubric.md](references/candidate-rubric.md): frequency, procedural stability, repeated inputs/outputs, judgment required, error cost, and cross-session value.
5. Classify each group as `skill`, `checklist/template`, `AI configuration`, or `manual/insufficient evidence`. A single occurrence is normally insufficient for a Skill unless the procedure is safety-critical and deterministic.
6. Record FACT (direct log evidence), INFERENCE (reasoning from evidence), and PROPOSAL (a future change). Do not claim that automation has improved outcomes before it is implemented and measured.
7. Produce a report at the user-specified path. If no output path is specified, return the report in the response rather than creating a repository file. Include the scanned root, logs inspected, candidate groups, scoring evidence, excluded candidates, uncertainties, and the highest-priority next action.

## Boundaries

- Do not treat the existence of a log entry as proof of repetition; count distinct dated occurrences or independently repeated inputs/outputs.
- Do not create a Skill solely to restate AGENTS.md, an existing Skill, or a project implementation plan.
- Prefer a checklist/template when the work has substantial human judgment but a stable set of prompts or review points.
- Prefer AI configuration only when the same cross-cutting omission persists across unrelated tasks and a repository-local Skill would be the wrong scope.
- Keep reports portable: use `<PROJECT_ROOT>`, `<REPO_ROOT>`, `<WORK_LOG_ROOT>`, `<DATE>`, and `<BRANCH_SLUG>` rather than absolute local paths.

## Output contract

Report the log root, files and date range inspected, normalized task groups, evidence counts, classification, recommended action, excluded or insufficient candidates, unresolved questions, and verification performed. State explicitly when no candidate has enough evidence.
