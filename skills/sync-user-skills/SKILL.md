---
name: sync-user-skills
description: Synchronize user skills from $HOME/.agents/skills to $HOME/.claude/skills. Use when adding, updating, reviewing, or mirroring skills shared by Codex and Claude Code, especially when the .agents directory is the source of truth.
---

# Sync User Skills

Treat `$HOME/.agents/skills` as the source of truth and mirror its skill directories into `$HOME/.claude/skills`.

## Safety rules

- Resolve both paths from `$HOME`; do not embed a user-specific absolute path.
- Review source and destination status before copying. Preserve unrelated existing changes.
- Copy only skill directories. Do not copy files placed directly in either skills root.
- Do not delete destination-only skills unless the user explicitly requests a complete mirror.
- Do not commit or push automatically. If either directory is Git-managed, show the diff and let the user review the commit.

## Synchronize

1. Resolve the source and destination. Accept explicit paths when the user provides them; otherwise use:

   ```powershell
   $source = "$HOME\.agents\skills"
   $destination = "$HOME\.claude\skills"
   ```

2. Confirm that the source exists and list top-level skill directories. Inspect destination-only directories before changing anything.

3. Preview the operation with `-WhatIf`:

   ```powershell
   & "$HOME\.agents\skills\sync-user-skills\scripts\sync_skills.ps1" `
     -SourcePath $source -DestinationPath $destination -WhatIf
   ```

4. After reviewing the preview, run the same command without `-WhatIf`. The script creates the destination and replaces matching destination skill directories with the source versions.

5. For a complete mirror, use `-PruneStale` only after confirming every destination-only skill may be removed. This is destructive and must never be the default.

6. Verify synchronization with a recursive file comparison. Report the source of truth, copied skills, preserved destination-only skills, any pruned skills, and the verification result.

## Verify

Use the bundled script's verification output, then independently confirm that every source file has the same relative path and content in the destination. Treat any mismatch as a failed synchronization.

## Commit handling

When the user asks to commit the synchronized changes, inspect the exact Git status and diff for the relevant repository first. Follow the repository's commit rules, use an English Conventional Commit message with a Why body, and never push automatically.
