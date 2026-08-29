---
name: plan-current-branch-work
description: Read a repository implementation plan and write a scoped Markdown work document for the currently checked-out branch without creating or switching branches. Use when the user wants the current branch's planned responsibilities extracted into an actionable checklist.
---

# Plan Current Branch Work

Turn the implementation plan's current-branch scope into a reviewable work document without changing Git branches.

## Determine the scope

1. Locate the user-provided implementation plan. If no path is provided, search tracked Markdown files for branch structure, branch order, or merge order and proceed only with a unique match.
2. Read the whole plan and directly linked specifications needed to interpret the current branch's responsibilities and completion criteria.
3. Inspect the repository root, current branch, status, and relevant history.
4. Match the exact current branch to the plan. Do not select a similarly named branch or infer scope from existing code alone. If the branch is not described, stop and report the mismatch.

## Write the branch work document

Create the document next to the implementation plan under `branch-plans/`. Convert `/` and other path separators in the branch name to `-`; for example, `feat/example-ui` becomes `branch-plans/feat-example-ui.md`.

Create or update only that branch's document. Preserve useful existing notes and completion evidence when updating it.

The document must contain:

- title and branch name;
- source implementation plan and specifications, using repository-relative links;
- prerequisites and dependencies;
- owned scope from the implementation plan;
- ordered, independently checkable work items using Markdown task boxes;
- explicit non-goals and responsibilities assigned to other branches;
- completion criteria and repository-defined verification commands that actually exist;
- unresolved decisions or blockers.

Use unchecked boxes for work not proven complete. Existing implementation may be cited as evidence, but do not mark an item complete merely because a related file exists. Separate source facts from inferred task decomposition, and do not invent requirements.

## Boundaries and verification

Do not create, switch, merge, rebase, delete, commit, or push branches. Do not edit the source implementation plan unless separately requested.

Before reporting, verify that links resolve, every task belongs to the current branch, the document does not absorb later-branch work, and unrelated files remain untouched. Report the document path and unresolved items.
