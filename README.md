<div id="top"></div>

# ai-skills-for-codex

Provide a Git-managed collection of reusable AI agent skills for development, testing, documentation, security, and repository workflows.

## Tech Stack

<p style="display: inline">
  <img src="https://img.shields.io/badge/-Markdown-000000.svg?style=for-the-badge" alt="Markdown">
  <img src="https://img.shields.io/badge/-YAML-000000.svg?style=for-the-badge" alt="YAML">
  <img src="https://img.shields.io/badge/-PowerShell-000000.svg?style=for-the-badge" alt="PowerShell">
  <img src="https://img.shields.io/badge/-Python-3776AB.svg?logo=python&style=for-the-badge&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/-Shell-000000.svg?style=for-the-badge" alt="Shell">
</p>

## Table of Contents

1. [About the Project](#about-the-project)
2. [Environment](#environment)
3. [Directory Structure](#directory-structure)
4. [Getting Started](#getting-started)
5. [Usage](#usage)
6. [Available Commands](#available-commands)

## About the Project

This repository stores reusable agent capabilities as Skills:

- `SKILL.md` defines a Skill's discovery metadata, purpose, workflow, and constraints.
- `agents/openai.yaml` provides optional UI metadata and invocation settings.
- `references/` keeps detailed guidance that is loaded only when needed.
- `scripts/` contains repeatable automation used by a Skill.
- `assets/` contains templates and other files used to produce outputs.

The `skills/` directory is the Git-managed source of truth for the collection. Individual Skills cover areas such as TDD, test design, frontend and backend engineering, security, Git and GitHub workflows, documentation, and synchronization between agent environments.

Each Skill is self-contained. Read its `SKILL.md` before using its scripts or supporting resources because the entrypoint defines the applicable safety rules and workflow.

<p align="right">(<a href="#top">back to top</a>)</p>

## Environment

| Language / Framework | Version |
| -------------------- | ------- |
| Markdown             | Not pinned |
| YAML                 | Not pinned |
| PowerShell           | Not pinned |
| Python               | Not pinned |
| POSIX shell          | Not pinned |

The repository has no root dependency manifest or lockfile. Runtime requirements are defined by the individual Skill and its scripts.

<p align="right">(<a href="#top">back to top</a>)</p>

## Directory Structure

```text
.
├── skills
│   ├── <skill-name>
│   │   ├── SKILL.md
│   │   ├── agents
│   │   ├── assets
│   │   ├── references
│   │   └── scripts
│   └── ...
└── README.md
```

Optional directories appear only when a Skill needs them.

### Main Directories

| Directory | Description |
| --------- | ----------- |
| `skills/` | Contains the reusable Skill packages managed by this repository. |

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

### Prerequisites

Install Git. PowerShell is also required to use the bundled synchronization scripts documented below. The repository does not pin tool versions.

### Clone the Repository

Clone the configured upstream into `$HOME/.agents`.

On Windows PowerShell:

```powershell
git clone git@github.com:kishimin-ai-create/ai-skills-for-codex.git "$HOME\.agents"
Set-Location "$HOME\.agents"
```

On macOS or Linux:

```bash
git clone git@github.com:kishimin-ai-create/ai-skills-for-codex.git "$HOME/.agents"
cd "$HOME/.agents"
```

No repository-wide dependency installation or build step is required. Inspect the selected Skill before running any Skill-specific script.

### Verify the Checkout

```powershell
git status --short --branch
Get-ChildItem "$HOME\.agents\skills" -Directory
```

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

### Invoke a Skill

Use the Skill name in an agent request when the client supports named Skill invocation:

```text
$test-case-design

Design test cases for this requirement.
```

### Inspect a Skill Before Use

```powershell
Get-Content "$HOME\.agents\skills\test-case-design\SKILL.md"
```

### Preview Synchronization with Claude Skills

The `sync-user-skills` Skill reconciles `$HOME/.agents/skills` with `$HOME/.claude/skills`. Preview the operation before applying it:

```powershell
$source = "$HOME\.agents\skills"
$destination = "$HOME\.claude\skills"

& "$HOME\.agents\skills\sync-user-skills\scripts\sync_skills.ps1" `
  -SourcePath $source -DestinationPath $destination -WhatIf
```

Review the preview and the `sync-user-skills/SKILL.md` safety rules before running the command without `-WhatIf`.

<p align="right">(<a href="#top">back to top</a>)</p>

## Available Commands

| Command | Description |
| ------- | ----------- |
| `git status --short --branch` | Shows the current branch and local changes. |
| `& "$HOME\.agents\skills\sync-user-skills\scripts\sync_skills.ps1" -SourcePath "$HOME\.agents\skills" -DestinationPath "$HOME\.claude\skills" -WhatIf` | Previews Skill reconciliation without copying files. |
| `& "$HOME\.agents\skills\sync-ai-skills-repository\scripts\sync_repository.ps1" -RepositoryPath "$HOME\.agents" -InspectOnly` | Fetches the configured upstream and reports whether the local or remote branch is ahead. |
| `python "$HOME/.agents/skills/portable-skill-paths/scripts/audit_skill_paths.py" "$HOME/.agents/skills"` | Audits Skill files for machine-specific paths without rewriting them. |

Read the owning Skill's `SKILL.md` before executing a bundled command. Some scripts inspect remote state or can modify files when their preview-only option is removed.

<p align="right">(<a href="#top">back to top</a>)</p>
