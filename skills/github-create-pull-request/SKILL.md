---
name: github-create-pull-request
description: pull-request-writingで作成・確認したPRタイトルと本文をそのまま使用し、GitHub MCPでPull Requestを安全に作成する。ユーザーがGitHub上へのPR作成・公開を明示的に依頼し、本文生成後にbase/headの確認、重複PRの検査、PR作成、URL確認まで行うときに使用する。
---

# GitHub Create Pull Request

`pull-request-writing` とPR公開を分離し、確認済みの文章をGitHub MCPへ正確に渡す。

## 責務境界

- ユーザーがPR作成を明示した場合だけ外部変更を行う。
- PR本文が未作成なら、最初に `pull-request-writing` を適用してドラフトだけを作成する。
- GitHub MCPを使用する。GitHub CLI、Web UI、REST APIの直接呼び出しは使用しない。
- コード、テスト、設定、Git履歴、PR本文を変更しない。作成確認後の一時ドラフト削除だけは、後述の条件で行う。
- `git commit`、`git push`、ブランチ作成を行わない。
- ブランチがGitHubに存在しない場合はPRを作成せず、pushが必要だと報告する。

## 1. 入力を確定する

1. `pull-request-writing` が作成したタイトルと本文を取得する。保存済みドラフトがある場合はファイルを読む。
2. タイトルまたは本文が未確定ならPRを作成せず、`pull-request-writing` で補う。
3. `git status --short --branch`、`git remote -v`、追跡ブランチを読み、repository、base、head候補を確認する。
4. ユーザー指定のrepository、base、head、draft状態を優先する。
5. 候補によってPR内容が変わる場合は、外部変更前にユーザーへ確認する。値を推測しない。

本文ファイルのパスやMarkdown記法をPR本文へ混ぜない。ファイル内容そのものを使用する。

## 2. 公開前条件を検証する

GitHub MCPで次を確認する。

1. repositoryへアクセスできる。
2. baseブランチとheadブランチがGitHub上に存在する。
3. headブランチにPR対象コミットが含まれる。
4. 同じrepository、base、headのopenなPRが存在しない。

重複確認にはGitHub MCPのPR検索を使い、headとbaseを絞り込む。検索結果が曖昧な場合は作成しない。

以下のいずれかなら停止し、不足条件を具体的に報告する。

- GitHub MCPを利用できない、または認証されていない
- repository、base、headを一意に確定できない
- headブランチがGitHubに存在しない
- 同じbase/headのopenなPRが既に存在する
- タイトルまたは本文が未確定

既存PRがある場合は新規作成せず、そのPRのURLを返す。

## 3. PRを作成する

すべての条件を満たした場合だけ、GitHub MCPのPull Request作成ツールを1回呼び出す。

- `repository_full_name`: 確認済みの `owner/name`
- `base`: 確認済みbaseブランチ
- `head`: 確認済みheadブランチ
- `title`: `pull-request-writing` が作成したタイトルを改変せず渡す
- `body`: `pull-request-writing` が作成した本文を改変せず渡す
- `draft`: ユーザー指定値。未指定なら `false`
- `maintainer_can_modify`: ユーザー指定がある場合だけ渡す

失敗時に条件を変えて自動再試行しない。エラーを確認し、同じPRが作成済みでないことをGitHub MCPで再検索してから報告する。

## 4. 作成結果を確認する

作成結果またはGitHub MCPのPR検索から、次を確認する。

- PR番号
- URL
- repository
- base ← head
- draft状態
- タイトル

本文がGitHub上で入力内容と一致することも、取得可能な範囲で確認する。

## 5. 公開済みの一時ドラフトを削除する

PRを作成し、GitHub MCPでrepository、base/head、タイトル、本文の一致を確認できた後、今回の入力として使用したローカルの一時本文Markdownを削除する。改行コードの違い以外の内容差がある場合は削除しない。

- 対象は `pull-request-writing` から渡された当該ファイルの正確なパス1件だけとする。`*.md`やディレクトリ単位では削除しない。
- 削除直前にも内容を読み直し、公開した本文と一致することを確認する。公開後に編集されていれば保持する。
- Gitで追跡されているファイル、利用者が保持を指定したファイル、今回の入力だと確認できないファイルは削除しない。
- 作成失敗、結果や本文の確認不能、重複PRの検出だけで終了した場合は保持する。
- 既にファイルがない場合はその事実を報告し、他のMarkdownを代わりに削除しない。
- 削除に失敗してもPRを再作成しない。PR作成の成功と、ローカル削除の失敗を分けて報告する。

## 完了報告

PRを作成した場合は、PR番号、タイトル、base ← head、draft状態、URL、一時ドラフトの削除結果（保持した場合は理由）を返す。

作成しなかった場合は、「PR未作成」と明記し、既存PRまたは不足条件を返す。ドラフトを保存しただけの状態をPR作成済みと表現しない。
