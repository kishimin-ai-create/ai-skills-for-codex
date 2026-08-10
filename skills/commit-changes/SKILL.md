---
name: commit-changes
description: Review Git changes, select only the intended files, and create a safe Conventional Commit with an English Why-focused body. Use when the user explicitly asks to commit completed work, prepare a commit, or turn reviewed changes into a Git commit.
---

# Commit Changes

Create a commit only after the user explicitly requests it. Review the complete change first, stage only the intended files, validate the message, and verify the resulting commit. Never push automatically.

## Review the repository

1. Confirm the repository root and current branch.
2. Inspect both unstaged and staged changes:

   ```powershell
   git status --short
   git diff
   git diff --staged
   git log -5 --oneline
   ```

3. Identify unrelated changes and preserve them. Do not use `git add .` or `git add -A`.
4. Exclude secrets, `.env` files, credentials, build output, dependency directories, and machine-specific files.

## Select and stage changes

Stage only the reviewed paths with explicit arguments:

```powershell
git add -- path/to/file another/path
```

Review the staged diff again:

```powershell
git diff --cached --check
git diff --cached
```

If multiple logical changes are present, split them into separate commits. Do not amend or rewrite a published commit.

## Write the commit message

Use this format:

```text
<type>: <imperative summary>

<Why this change is valuable>
```

- Write the message in English.
- Keep the imperative summary under 50 characters.
- Choose a matching Conventional Commit type: `feat`, `fix`, `refactor`, `docs`, `test`, or `chore`.
- Explain why the change matters in the body; do not merely describe the implementation.
- Never use a summary-only message.

For PowerShell, pass the subject and body separately:

```powershell
git commit -m "feat: add export validation" `
  -m "Prevent invalid exports from reaching downstream consumers."
```

Read `$HOME/.agents/skills/git-rules/references/commit-message-rules.md` in full immediately before committing and apply its validation criteria.

## Commit and verify

Run the commit without `--no-verify`. If a hook fails, fix the cause, restage the intended files, and create a new commit; do not bypass the hook.

```powershell
git commit -m "<type>: <imperative summary>" -m "<Why body>"
git status --short
git show --stat --oneline --summary HEAD
```

Report the commit hash, message, changed files, and verification result. Do not run `git push`; leave remote publication for the user.
