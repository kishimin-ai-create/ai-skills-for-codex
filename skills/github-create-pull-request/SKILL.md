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
- コード、テスト、設定、Git履歴、PR本文を変更しない。
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

## 完了報告

PRを作成した場合は、PR番号、タイトル、base ← head、draft状態、URLを返す。

作成しなかった場合は、「PR未作成」と明記し、既存PRまたは不足条件を返す。ドラフトを保存しただけの状態をPR作成済みと表現しない。
