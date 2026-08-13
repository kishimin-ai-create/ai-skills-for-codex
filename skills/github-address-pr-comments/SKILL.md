---
name: github-address-pr-comments
description: GitHub Pull RequestのレビューThread、Review本文、ConversationコメントをGitHub MCPで取得し、指摘の妥当性を検証して、必要なコード・テスト・文書修正、検証、コミット、PRブランチへの反映、返信、Thread解決まで行う。PRコメントへの返答、requested changesへの対応、レビュー指摘の修正を依頼されたときに使用する。
---

# GitHub Address PR Comments

PRコメントを事実と変更結果へ照合し、必要な修正と返信を最後まで一致させる。GitHubの読み書きにはGitHub MCPだけを使用する。

## 1. 対象を確定する

1. 対象リポジトリの`AGENTS.md`、関連ADR、必須Skillを読む。
2. `git status --short --branch`、remote、upstreamを確認し、既存のローカル変更を保護する。
3. ユーザー指定のPR URLまたは番号を優先する。未指定なら、現在ブランチとGitHub MCPのPR検索からbase/headが一致するPRを一意に解決する。
4. PRのhead SHAとローカルHEADを比較する。不一致のまま別の履歴へ修正を加えない。

## 2. コメントを取得する

GitHub MCPから次をすべて取得する。

- 未解決を含むReview Threadと全返信
- Review本文と状態（approved、changes requested、commented）
- Conversationのトップレベルコメント
- Threadのpath、line、outdated、resolved状態
- PRのbase、head、head SHA、draft、mergeable状態

平坦なコメント一覧だけでThreadの未解決状態を推測しない。Botの結果通知と、人間が対応を求めるコメントを区別する。

## 3. 指摘を検証して分類する

`validate-review-findings`を適用し、完全な差分、周辺コード、仕様、ADR、テスト、呼び出し元へ照合する。各コメントを次のいずれかへ分類する。

- `NEEDS_FIX`: 変更が導入した再現可能な欠陥または契約違反で、修正が必要。
- `NEEDS_REPLY`: 質問、説明要求、誤解、または変更不要と根拠を示せる指摘。
- `NEEDS_DECISION`: 仕様が不足・矛盾し、人間の判断なしに修正方法を確定できない。
- `NO_ACTION`: 解決済み、outdated、重複、Bot通知、または対象外。

レビューコメントを自動的に正しいと仮定しない。反対に、変更が面倒という理由で退けない。複数コメントが同じ根本原因なら、重複関係を記録して一つの修正へまとめる。

## 4. 必要な修正を行う

`NEEDS_FIX`ごとに`fix-patterns`と`tdd`を適用する。

1. 修正前に最小の再現テストまたは決定的な検証を追加し、Redを確認する。
2. 最小修正でGreenにする。
3. 必要な場合だけ、Greenを維持してリファクタリングする。
4. 対象テスト、関連テスト、全体テスト、build、lint、型検査、カバレッジをリスクに応じて実行する。
5. 指摘と無関係な変更を混ぜず、`git-rules`に従って論理的な単位でコミットする。

テストを弱める、例外を握りつぶす、仕様を推測で変更する、他者の変更を破棄する修正は禁止する。

## 5. PRブランチへ反映する

返信で「修正済み」と述べる前に、修正コミットがGitHub上のPR headへ存在することを確認する。

- pushがユーザーの依頼または適用Skillで許可されている場合だけ、forceなしでPRのheadと同名のremote refへpushする。
- fork、権限不足、head不一致、保護規則、未許可のpushで反映できない場合は停止し、ローカル修正と未反映状態を報告する。
- force push、rebaseによる共有履歴の書き換え、baseブランチへの直接pushを行わない。

## 6. GitHubへ返信する

GitHub MCPで、元コメントの種類に対応する場所へ返信する。

- Review ThreadにはThread返信を使う。
- Conversationコメントにはトップレベル返信を使い、対象コメントを明示する。
- Review本文に個別Threadがない場合はConversationへまとめて返信する。

返信には分類に応じて次を含める。

- `NEEDS_FIX`: 根本原因、修正内容、PR上のコミット、実行した検証と結果。
- `NEEDS_REPLY`: 変更しない結論と、仕様・ADR・コード・テストの具体的根拠。
- `NEEDS_DECISION`: 確定できない点と、必要な判断を一つの明確な質問として示す。

内部の絶対パス、秘密情報、巨大なログを含めない。未pushの変更を「対応済み」と表現しない。

## 7. Threadを解決して再確認する

次の条件を満たすReview ThreadだけをGitHub MCPで解決する。

- `NEEDS_FIX`: 修正コミットがPR headへ反映済みで、関連検証が成功し、返信済み。
- `NEEDS_REPLY`: 変更不要の根拠を返信済みで、追加判断を待たない。

`NEEDS_DECISION`は解決しない。ConversationコメントやReview本文をThreadとして解決しようとしない。

最後にコメントとThreadを再取得し、返信本文、返信先、resolved状態、PR head SHAを確認する。

## 完了報告

次を区別して報告する。

- 修正・返信・判断待ち・対象外の各コメント
- 変更ファイル、コミット、push先
- 検証コマンドと結果
- 解決したThreadと未解決Thread
- 残存リスクと未反映のローカル変更

返信案だけを求められた場合はGitHubへ書き込まず、分類と返信案を返す。

## Safety

- GitHubへの返信・Thread解決は、ユーザーがコメント対応を依頼した場合だけ行う。
- PRをマージ、close、approve、request changesへ変更しない。別途明示された依頼が必要。
- GitHub CLI、Web UI、直接REST API、独自GraphQLスクリプトへ切り替えない。
- 同じ返信や修正を重複投稿・重複コミットしない。
