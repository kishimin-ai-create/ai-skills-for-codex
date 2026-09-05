---
name: sync-ai-skills-repository
description: Synchronize the Git-managed $HOME/.agents skill collection with its upstream ai-skills-for-codex repository. Use when comparing, pulling, or preparing to publish whichever Git side has advanced without overwriting divergence.
---

# Sync AI Skills Repository

Synchronize the dedicated Skill repository at `$HOME/.agents` with its configured upstream. Confirm the actual remote URL instead of inferring an owner from a shorthand repository name.

## Direction rule

Use the Git commit graph, not timestamps:

- `IN_SYNC`: do nothing.
- `REMOTE_AHEAD`: fast-forward the local branch with `--ff-only`.
- `LOCAL_AHEAD`: preserve local commits and report the exact push command for human execution; do not push automatically.
- Both ahead and behind: stop as diverged. Do not merge, rebase, reset, or choose a side automatically.
- Dirty worktree: stop before fetching or copying.

## Workflow

1. Resolve the repository path, defaulting to `$HOME/.agents`.
2. Inspect `git status --short --branch`, `git remote -v`, the current branch, and its upstream.
3. Preview the direction:

   ```powershell
   & "$HOME\.agents\skills\sync-ai-skills-repository\scripts\sync_repository.ps1" `
     -RepositoryPath "$HOME\.agents" -InspectOnly
   ```

4. If the result is `REMOTE_AHEAD`, rerun without `-InspectOnly`. The script fetches and fast-forwards only.
5. If the result is `LOCAL_AHEAD`, review the commits and provide `git push origin <branch>` for the user to run. Never execute it automatically.
6. After a remote-to-local update, invoke `sync-user-skills` to reconcile `$HOME/.agents/skills` and `$HOME/.claude/skills` by their newer contents.
7. Verify the final ahead/behind counts and report any unpublished commits or divergence.

## Safety

- Never use force push, hard reset, automatic rebase, or an automatic merge for divergence.
- Never interpret a larger commit timestamp as newer history; ancestry determines progress.
- Do not publish secrets, machine-specific paths, or unrelated worktree changes.
- A local-ahead result is prepared for publication, not fully synchronized, until the user performs the push.
