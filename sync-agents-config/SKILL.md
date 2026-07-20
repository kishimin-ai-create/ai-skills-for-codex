---
name: sync-agents-config
description: Synchronize a Git-managed AGENTS.md from a dedicated repository with $HOME/.codex/AGENTS.md. Use when creating, pulling, reviewing, or publishing a standalone AGENTS.md configuration repository without changing an application repository or using .gitignore to hide its structure.
---

# Sync Agents Config

Treat the dedicated repository's root `AGENTS.md` as the only source of truth. Copy it to `$HOME/.codex/AGENTS.md` after a pull or local update, and verify both files match.

Default the dedicated repository to `$HOME/agents-config` when the user does not provide another path. Do not create or modify an application repository, `.gitignore`, or a remote repository unless the user explicitly requests that separate action.

## Sync from the repository

1. Resolve the dedicated repository path and confirm it is the intended repository.
2. Confirm the repository contains the expected root file and inspect its status:

   ```powershell
   Set-Location "$HOME\agents-config"
   git status --short
   Test-Path .\AGENTS.md
   git ls-files
   ```

3. Pull only after confirming the remote and branch are correct. Never force-push, rewrite shared history, or push automatically:

   ```powershell
   git remote -v
   git pull --ff-only
   ```

4. Copy the repository file to Codex's active configuration:

   ```powershell
   Copy-Item -LiteralPath "$HOME\agents-config\AGENTS.md" `
     -Destination "$HOME\.codex\AGENTS.md" -Force
   ```

5. Verify the copy using hashes:

   ```powershell
   (Get-FileHash "$HOME\agents-config\AGENTS.md").Hash
   (Get-FileHash "$HOME\.codex\AGENTS.md").Hash
   ```

The hashes must match before reporting synchronization complete.

## Publish a local update

1. Edit only the repository's root `AGENTS.md`.
2. Review the diff and confirm the file contains no secrets, tokens, personal data, or machine-specific absolute paths. Use `$HOME/...` for user-home paths.
3. Confirm only `AGENTS.md` is tracked or changed:

   ```powershell
   git status --short
   git diff -- AGENTS.md
   git ls-files
   ```

4. Commit with a reason-focused message, for example:

   ```powershell
   git add AGENTS.md
   git commit -m "docs: update shared agent instructions"
   ```

5. Do not run `git push` automatically. Provide the exact push command for the user to review and run:

   ```powershell
   git push origin <branch>
   ```

6. After the user confirms the remote update, run the sync step above if the local Codex file should reflect the committed version.

## Initialize a dedicated repository

When the dedicated repository does not exist, create it separately from any application repository. Copy `$HOME/.codex/AGENTS.md` into its root, initialize Git, and verify that only `AGENTS.md` is tracked:

```powershell
New-Item -ItemType Directory -Force "$HOME\agents-config"
Copy-Item -LiteralPath "$HOME\.codex\AGENTS.md" `
  -Destination "$HOME\agents-config\AGENTS.md" -Force
Set-Location "$HOME\agents-config"
git init
git add AGENTS.md
git status --short
git ls-files
```

Do not create a `.gitignore` merely to conceal other files. Do not create a GitHub repository or push changes without explicit user authorization; when authorized, still leave the final push for the user's review according to the Git rules.
