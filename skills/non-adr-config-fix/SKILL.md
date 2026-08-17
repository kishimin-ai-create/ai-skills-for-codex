---
name: non-adr-config-fix
description: Diagnose and safely fix configuration, CI workflow, environment, and tool-setting defects that do not require an architecture decision record. Use when a known setting, filter, path, threshold, option, or operational rule needs a minimal repository change with reproducible validation.
---

# Non-ADR Configuration Fix

## Overview

Use this skill for a small, evidence-backed change to configuration or operational settings when the intended behavior is already known and no new architectural decision is being made. Typical targets are CI workflow filters, test thresholds, environment-specific option values, tool configuration, and repository scripts.

## Scope Gate

Before editing, classify the request:

- Continue when the desired value or rule is already specified by an existing contract, ADR, issue, review finding, or failing check.
- Stop and use `adr-writing` when the change selects a new boundary, dependency, lifecycle, public contract, test strategy, or reusable policy not already decided.
- Do not treat a user's one-off wording or a formatting preference as a design decision.

Record the applicable ADR and the evidence for the intended setting. Never use this skill to hide an unresolved design choice.

## Workflow

1. **Inspect the boundary**
   - Read repository instructions and applicable ADRs before editing.
   - Check branch, remote, upstream, and worktree status; preserve unrelated changes.
   - Locate the authoritative setting and every validator, consumer, and duplicate declaration.

2. **Reproduce the defect**
   - Prefer a deterministic failing check, test, CI guard, or command that demonstrates the current setting is wrong.
   - Capture the expected and actual behavior without exposing secrets.
   - If the existing guard is too weak, strengthen it first so the old configuration fails.

3. **Apply the smallest configuration change**
   - Edit only the source-of-truth configuration and required validation scripts or tests.
   - Keep event filters, environment names, paths, and thresholds explicit.
   - Do not commit secrets, local machine files, generated output, or unrelated refactors.

4. **Verify Green**
   - Run the new guard and the affected tests or build.
   - Run the full relevant validation when the setting affects CI, dependency wiring, or runtime startup.
   - Check formatting, YAML/JSON syntax, warnings, and the final diff.

5. **Record and deliver**
   - Use an English Conventional Commit with a Why body.
   - Summarize the setting changed, evidence, validation results, and residual assumptions.
   - Push only when the active workflow explicitly permits it; never push directly to a shared branch.

## Common Checks

For CI configuration, verify both the normal test matrix and every coverage/reporting invocation. A filter present in one job does not constrain another job that starts its own test runner.

For application configuration, verify the source of values (committed defaults, environment variables, options binding, and validation timing) and test both valid and missing/invalid values.

For path or endpoint settings, test URI combination with and without a base path, and avoid changing a public contract merely to simplify a setting.

## Completion Criteria

- The old configuration was reproduced as failing or the existing guard was proven deterministic.
- The minimal setting change passes targeted and relevant full checks.
- No ADR-worthy decision was smuggled into a configuration patch.
- The worktree and commit contain only intended files.
- The final report distinguishes facts, inferences, assumptions, and any unpushed changes.
