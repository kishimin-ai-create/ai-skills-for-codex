---
name: sync-agents-config
description: Synchronize a Git-managed AGENTS.md with $HOME/.codex/AGENTS.md. Use when either copy may have advanced and the newer content must be preserved while remote Git history remains protected.
---

# Sync Agents Config

Keep the dedicated repository's root `AGENTS.md` and `$HOME/.codex/AGENTS.md` equal. After fetching the repository, compare hashes and update times and copy the changed/newer file over the older one. Equal timestamps with different content are a conflict and must not be resolved automatically.

Default the dedicated repository to `$HOME/agents-config` when the user does not provide another path. Do not create or modify an application repository, `.gitignore`, or a remote repository unless the user explicitly requests that separate action.

## Determine the synchronization direction

1. Resolve the dedicated repository path and confirm it is the intended repository.
2. Confirm the repository contains the expected root file and inspect its status:

   ```powershell
   Set-Location "$HOME\agents-config"
   git status --short
   Test-Path .\AGENTS.md
   git ls-files
   ```

3. Fetch and compare the current branch with its upstream. Fast-forward only when the remote is ahead. If both sides advanced, stop before comparing files:

   ```powershell
   git remote -v
   git fetch --prune
   git rev-list --left-right --count HEAD...@{upstream}
   ```

4. Compare hashes. If they differ, use `LastWriteTimeUtc` to select the newer file. If times are equal, stop as a conflict.
5. Copy the newer file to the older location. For example, repository to active configuration:

   ```powershell
   Copy-Item -LiteralPath "$HOME\agents-config\AGENTS.md" `
     -Destination "$HOME\.codex\AGENTS.md" -Force
   ```

6. Verify the copy using hashes:

   ```powershell
   (Get-FileHash "$HOME\agents-config\AGENTS.md").Hash
   (Get-FileHash "$HOME\.codex\AGENTS.md").Hash
   ```

The hashes must match before reporting synchronization complete.

## Repository-ahead handling

When `$HOME/.codex/AGENTS.md` is newer, copy it into the repository and review the resulting diff. Commit only the repository's root `AGENTS.md`.

1. Review the diff and confirm the file contains no secrets, tokens, personal data, or machine-specific absolute paths. Use `$HOME/...` for user-home paths.
2. Confirm only `AGENTS.md` is tracked or changed:

   ```powershell
   git status --short
   git diff -- AGENTS.md
   git ls-files
   ```

3. Commit with a reason-focused message, for example:

   ```powershell
   git add AGENTS.md
   git commit -m "docs: update shared agent instructions"
   ```

4. Do not run `git push` automatically. Provide the exact push command for the user to review and run:

   ```powershell
   git push origin <branch>
   ```

5. After the user confirms the remote update, fetch and verify that the repository, upstream, and active file agree.

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
