---
name: plan-next-branch-work
description: Read a repository implementation plan, identify the next explicitly ordered branch, create it from the plan-defined start point, and write that branch's scoped work plan as Markdown. Use when the user asks to move from the current branch to the next planned branch; do not use merely to inspect the current branch.
---

# Plan Next Branch Work

Move development to the next work unit defined by an implementation plan and leave a reviewable branch work document.

## Resolve the plan and branch

1. Locate the implementation plan from the user-provided path. If none is provided, search tracked Markdown files for branch structure, branch order, or merge order and use a unique match only.
2. Read the whole plan and any directly linked specifications needed to understand the next branch's scope and completion criteria.
3. Inspect the repository root, current branch, status, local branches, and relevant ancestry. Preserve unrelated changes.
4. Match the current branch to the plan's explicit branch sequence. Select only its immediate successor. Do not infer a successor from branch names or invent one after the final planned branch.
5. Resolve the successor's start point from the plan. If the plan requires a parent or prerequisite branch, confirm that the chosen start point contains the required work. Do not silently branch from the current branch when the plan defines sibling branches.

Stop without switching branches when the plan is ambiguous, the current branch is absent from its order, required work is not present at the start point, the target branch already exists with an unclear state, or local changes would be carried across branches. Report the exact condition that must be resolved.

## Create the branch

Branch creation is authorized only when the user asks to create or move to the next branch. Create the exact plan-defined branch with a non-interactive Git command. Never push, merge, rebase, delete branches, or modify the implementation plan unless separately requested.

After creation, confirm the checked-out branch and its start commit.

## Write the branch work document

Create the document next to the implementation plan under `branch-plans/`. Convert `/` and other path separators in the branch name to `-`; for example, `feat/example-ui` becomes `branch-plans/feat-example-ui.md`.

The document must contain:

- title and branch name;
- source implementation plan and specifications, using repository-relative links;
- start point, prerequisites, and dependencies;
- owned scope copied or faithfully paraphrased from the plan;
- ordered, independently checkable work items using unchecked Markdown task boxes;
- explicit non-goals and work owned by other branches;
- branch completion criteria and the repository-defined verification commands that actually exist;
- unresolved decisions or blockers.

Distinguish plan facts from implementation inferences. Label inferred decomposition as such and do not add product behavior that the source documents do not require. Do not mark work complete while generating the plan.

## Verify and report

Confirm the file is on the new branch, links resolve, every task belongs to the branch scope, and no unrelated files changed. Report the new branch, start point, document path, and any unresolved items.
