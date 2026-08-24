---
name: sync-user-skills
description: Synchronize shared user skills between $HOME/.agents/skills and $HOME/.claude/skills. Use when either copy may have advanced and the newer skill directory must be preserved without hiding conflicts.
---

# Sync User Skills

Keep `$HOME/.agents/skills` and `$HOME/.claude/skills` equal while preserving whichever copy of each Skill advanced.

## Safety rules

- Resolve both paths from `$HOME`; do not embed a user-specific absolute path.
- Review source and destination status before copying. Preserve unrelated existing changes.
- Copy only skill directories. Do not copy files placed directly in either skills root.
- A directory present on only one side is a new Skill and is copied to the other side; it is not treated as a deletion.
- For a Skill present on both sides, compare content hashes first and the newest recursive file timestamp second. Copy the newer directory over the older one.
- If content differs but newest timestamps are equal, stop and report a conflict. Do not choose a side.
- Do not infer deletion from absence. Remove a Skill only through a separate explicit deletion request.
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

5. The legacy `-PruneStale` switch is rejected because absence cannot distinguish a deletion from a newly added Skill on the other side.

6. Verify synchronization with recursive path and content hashes. Report the direction chosen for each changed Skill and any conflicts.

## Verify

Use the bundled script's verification output, then independently confirm that both roots contain the same Skill directories and that corresponding relative paths and hashes match. Treat any mismatch as a failed synchronization.

## Commit handling

When the user asks to commit the synchronized changes, inspect the exact Git status and diff for the relevant repository first. Follow the repository's commit rules, use an English Conventional Commit message with a Why body, and never push automatically.
