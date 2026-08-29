---
name: verify-branch-plan-completion
description: Audit a branch work Markdown document against its implementation plan, repository changes, and available verification results, then write an evidence-based completion report. Use after planned branch work is believed complete; do not use to implement missing work.
---

# Verify Branch Plan Completion

Decide whether the current branch has completed its assigned plan without changing implementation code.

## Gather evidence

1. Locate the implementation plan and the current branch document under its sibling `branch-plans/` directory. If either is ambiguous or missing, stop and identify what is needed.
2. Read both documents in full, plus directly linked specifications governing the branch scope and completion criteria.
3. Inspect the repository root, current branch, status, diff from the plan-defined start point, commits, and relevant generated or configured artifacts.
4. Discover verification commands only from repository configuration and documentation. Run all commands required by the branch completion criteria that are available and safe in the local repository. Do not invent commands, push, or mutate external systems.

Treat task-box state as a claim, not evidence. Verify behavior-oriented items using tests or observable artifacts, structural items using the relevant files, and exclusions by checking that later-branch responsibilities were not introduced.

## Classify each item

For every work item and completion criterion, record one status:

- `PASS`: direct repository or command evidence proves it;
- `FAIL`: evidence contradicts it or a required verification fails;
- `BLOCKED`: required evidence cannot be obtained because a declared dependency or tool is unavailable;
- `NOT VERIFIED`: evidence is absent or insufficient.

Include concise evidence such as a repository-relative file link, commit, or command result. Never convert `BLOCKED` or `NOT VERIFIED` into `PASS`, and do not accept unrelated pre-existing failures as proof that branch work is complete.

## Write the completion report

Write `branch-plans/<branch-file-stem>.completion.md` next to the branch work document. Include:

- branch, checked commit, plan, and work-document references;
- overall result: `COMPLETE` only when every required item and criterion is `PASS`, otherwise `INCOMPLETE`;
- a table of every item with status and evidence;
- verification commands, exit results, and relevant summaries such as coverage;
- out-of-scope changes, remaining work, blockers, and pre-existing failures;
- the exact next action needed for each non-passing item.

Do not edit implementation files or mark task boxes complete unless the user separately asks. Do not commit or push. Report the overall result and completion-report path.
