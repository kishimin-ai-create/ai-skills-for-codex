---
name: sync-claude-codex
description: $HOME/.claude/CLAUDE.md と $HOME/.codex/AGENTS.md を同期する。どちらかを編集した後、もう一方へ変更を反映するときに使う。
---

# Sync Claude ↔ Codex

`$HOME/.claude/CLAUDE.md`（Claude Code用）と`$HOME/.codex/AGENTS.md`（Codex/他エージェント用）を同期する。

## 前提

- 両ファイルは同一内容を保つことを原則とする。
- どちらかを更新したら、このSkillでもう一方へ反映する。
- 同期はファイルコピーで行い、変更が進んだファイルをもう一方へ反映する。
- 内容が異なるのに更新日時が同じ場合は競合として停止し、自動選択しない。

## 手順

### 1. 現状を確認する

```powershell
$claudeMd = "$HOME\.claude\CLAUDE.md"
$agentsMd = "$HOME\.codex\AGENTS.md"

Test-Path $claudeMd
Test-Path $agentsMd
```

両ファイルが存在しない場合は、存在するほうをコピーして作成する。

### 2. 差分を確認する

```powershell
Compare-Object (Get-Content $claudeMd) (Get-Content $agentsMd)
```

出力がなければ同一。差分がある場合は内容を確認してから同期方向を決める。

### 3. 同期方向を決める

ユーザーが方向を指定していない場合は、内容のハッシュを先に比較する。異なる場合は更新日時が新しいほうを採用し、採用したファイルを報告する。更新日時も同じなら競合として停止する。

```powershell
(Get-Item $claudeMd).LastWriteTime
(Get-Item $agentsMd).LastWriteTime
```

### 4. コピーして同期する

#### CLAUDE.md → AGENTS.md の場合

```powershell
Copy-Item -LiteralPath $claudeMd -Destination $agentsMd -Force
```

#### AGENTS.md → CLAUDE.md の場合

```powershell
Copy-Item -LiteralPath $agentsMd -Destination $claudeMd -Force
```

### 5. 同一性を検証する

```powershell
$h1 = (Get-FileHash $claudeMd).Hash
$h2 = (Get-FileHash $agentsMd).Hash
if ($h1 -eq $h2) { "OK: 両ファイルは一致しています" } else { "ERROR: ハッシュが一致しません" }
```

ハッシュが一致した場合のみ同期完了を報告する。

## 完了報告

- 同期方向（どちらを正としたか）
- コピー前の差分の有無
- ハッシュ検証の結果
- 同期後の両ファイルパス
