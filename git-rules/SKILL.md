---
name: git-rules
description: Gitのブランチ命名、履歴保護、リモート操作の制限、コミット対象を管理し、安全にGit操作を行うためのルール。
---

# Git Rules

## 目的

Git のブランチ、履歴、コミット対象を安全に管理すること。

## 手順

### 1. ブランチ名を決定する

ブランチ名は `{type}/{short-description}` の形式を使用する。

例:

- `feat/add-auth`
- `fix/null-guard`
- `refactor/clean-interactor`

description には kebab-case を使用する。

type は Conventional Commits に合わせ、以下を使用する。

- `feat`
- `fix`
- `refactor`
- `docs`
- `test`
- `chore`

### 2. Git 履歴を保護する

`main` または共有ブランチに force push してはならない。

`git push` またはリモートへ書き込むその他のコマンドを実行してはならない。

リモートへの push は、人間または明示的に許可された別のワークフローに任せる。

すでに共有ブランチへ push されたコミットを、rebase、amend、squash によって書き換えてはならない。

PR を作成する前であれば、自分の feature ブランチで rebase / squash を行ってもよい。

### 3. コミット対象を確認する

明示的に必要とされない限り、以下をコミットしてはならない。

- `node_modules/`
- ビルド出力（`dist/`、`build/`）
- その他の生成物

`.env` ファイルや、シークレットまたは認証情報を含むファイルをコミットしてはならない。

代わりに、プレースホルダー値を使用した `.env.example` を使用する。

以下のようなマシン固有のファイルをコミットしてはならない。

- `.DS_Store`
- `Thumbs.db`
- チームで共有しない IDE 設定ファイル

## 参照

- コミットする時に書きを必ず参照しなさい。
- []()