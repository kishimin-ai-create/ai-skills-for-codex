---
name: git-branch-naming
description: Gitブランチの種類、名前、起点を決定し、既存規約との不整合を防ぐ。新しいブランチの作成・提案・改名、ブランチ計画の作成、Git命名規則の設計やレビューを行うときに使用する。
---

# Git Branch Naming

## 手順

1. リポジトリの `AGENTS.md`、ADR、開発計画、既存ブランチを確認する。
2. 変更の主目的を一つ選ぶ。
3. `{type}/{short-description}` 形式の名前を決める。
4. 既存規約や文書と名前が矛盾する場合は、ブランチを作る前に情報源を統一する。

## Type

- 新しい利用者向け機能またはドメイン機能には `feature/` を使用する。
- 不具合修正には `fix/` を使用する。
- 外部の振る舞いを変えない構造改善には `refactor/` を使用する。
- 文書だけの変更には `docs/` を使用する。
- テストだけの変更には `test/` を使用する。
- 保守作業には `chore/` を使用する。

`feat/` はブランチ名に使用しない。`feat:` は Conventional Commits のコミット種別として使用し、機能ブランチを表す `feature/` と役割を分ける。

## Description

- 小文字の kebab-case を使用する。
- 実装方法ではなく、達成する変更を簡潔に表す。
- `update`、`changes`、`work` だけの曖昧な名前を避ける。
- チームがIssue番号を要求する場合は、descriptionの先頭へ含める。

例:

- `feature/add-render-text-model`
- `feature/123-add-render-text-model`
- `fix/reject-invalid-hex-color`
- `refactor/simplify-color-validation`

## 運用

- 変更に必要な最も近い安定ブランチから作成する。
- 一つのブランチへ無関係な目的を混在させない。
- ブランチを短命に保ち、マージ後に削除する。
- TDDの `test:`、`feat:`、`refactor:` コミットは、同じ `feature/` または `fix/` ブランチへ積む。
- リモート操作と履歴保護には `git-rules` を適用する。
