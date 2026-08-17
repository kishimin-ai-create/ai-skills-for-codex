---
name: github-handle-pr-comments
description: GitHub Pull Requestの未解決レビューThreadと会話コメントを調査し、指摘を返信のみまたは修正必須に分類して、必要なコード・テスト・文書修正、検証、コミット、GitHub返信、Thread解決まで行う。ユーザーがPRコメントへの返答、レビュー指摘への対応、requested changesの解消、またはコメントを確認して必要なら修正するよう依頼したときに使用する。
---

# GitHub PR Comment Handler

PRコメントへ、実際の変更と検証結果に一致する返信を行う。Thread状態の取得にはGitHub GraphQLを使い、平坦なコメント一覧だけで判断しない。

## 1. Contextを解決する

1. 対象リポジトリの`AGENTS.md`、関連ADR、必須Skillを先に読む。
2. `git status --short --branch`でローカル変更を確認し、ユーザーの変更を保護する。
3. ユーザー指定のPR URLまたは番号を優先する。未指定なら現在のブランチから`gh pr view --json number,url,title,headRefName,baseRefName`で解決する。
4. `gh auth status`が失敗したら書き込みを行わず、認証を依頼する。

## 2. コメントを取得する

次を実行する。リポジトリとPRを自動解決できない場合だけ`--repo OWNER/REPO --pr NUMBER`を渡す。

```powershell
python "$HOME/.codex/skills/github-handle-pr-comments/scripts/fetch_pr_comments.py"
```

スクリプトの`review_threads`から`isResolved`、`isOutdated`、ファイル、行、全返信を確認する。会話コメントとReview本文は補助情報として扱う。

## 3. 指摘を分類する

未解決かつ最新のThreadを、重複をまとめて次へ分類する。

- `NEEDS_FIX`: 差分が導入した再現可能な不具合、契約矛盾、セキュリティ、性能、保守性の問題。コード・テスト・文書の変更が必要。
- `NEEDS_REPLY`: 質問、説明要求、誤解、方針確認、または変更不要と根拠を示せる指摘。
- `WAITING`: 指摘が曖昧、相互に矛盾、または仕様判断が必要。推測で修正せずユーザーへ判断を求める。
- `NO_ACTION`: 解決済み、古いThread、Botの結果通知、重複済みの指摘。

指摘本文だけで受け入れず、完全な差分、周辺コード、仕様、テスト、呼び出し元から妥当性を確認する。

## 4. 必要な修正を行う

`NEEDS_FIX`ごとに次を行う。

1. 期待する振る舞いを再現する失敗テストまたは決定的な検証を用意し、Redを確認する。
2. 最小修正でGreenにする。
3. 対象テスト、関連テスト、リポジトリのlint・型検査・全体テストをリスクに応じて実行する。
4. 適用されるGit規則が要求する場合だけ、指摘単位または論理的変更単位でコミットする。

レビューを通すためにテストを弱めない。指摘と無関係な変更を混ぜない。`git push`はユーザーまたは適用規則が明示的に許可した場合だけ行う。

## 5. GitHubへ返信する

ユーザーが返信を依頼した場合だけ書き込む。Review Threadへの返信には次のGraphQL mutationを使う。

```graphql
mutation($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(
    input: {pullRequestReviewThreadId: $threadId, body: $body}
  ) {
    comment { id url }
  }
}
```

返信は簡潔にし、次を含める。

- `NEEDS_FIX`: 何を直したか、関連テスト結果、PR上で参照できるコミット。未pushなら「対応済み」と断言せず、ローカル修正であることを明示する。
- `NEEDS_REPLY`: 変更しない理由を、仕様・コード・テストの具体的根拠とともに説明する。
- `WAITING`: 不明点と、必要な判断を1つの明確な質問として返す。

将来対応の約束だけで解決扱いにしない。秘密情報、巨大なログ、内部パスを返信へ含めない。

## 6. Threadを解決して検証する

次の場合だけ`resolveReviewThread`を実行する。

- 修正コミットがPRのheadへ反映済みで、検証が成功している。
- 返信だけで完結する指摘について、根拠を返信済みである。

返信・解決後に取得スクリプトを再実行し、返信者、本文、`isResolved`を確認する。最後に次を報告する。

- 対応・返信・保留・対象外のThread
- 変更ファイルとコミット
- 実行した検証と結果
- pushされていない変更、未解決Thread、残存リスク

## Safety

- ユーザーが返信を依頼していない場合は、返信案だけを作りGitHubへ書き込まない。
- ユーザーが解決を依頼していない場合でも、返信依頼だけからThread解決まで推測しない。
- forkまたはDependabot PRでToken権限が不足する場合、`pull_request_target`へ安易に切り替えない。
- force push、履歴書き換え、他者の変更の破棄を行わない。

## Resource

- `scripts/fetch_pr_comments.py`: PR会話コメント、Review、Review Threadの状態と行アンカーをGraphQLで取得する。
