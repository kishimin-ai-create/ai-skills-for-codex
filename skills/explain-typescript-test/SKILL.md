---
name: explain-typescript-test
description: 指定されたTypeScriptのテストファイルを、テスト対象、テスト名、Arrange・Act・Assert、各matcher、Vitest・Jest・Testing Library・MSW・Playwrightの機能、フロントエンドまたはNode.js境界との関係に分解して日本語で説明する。ユーザーが.test.ts、.test.tsx、.spec.ts、.spec.tsxなどについて、処理内容、意図、保証する振る舞い、todo・skip理由、parameterized test、fixture、mock、stubの役割を知りたいときに使用する。
---

# Explain TypeScript Test

指定されたTypeScriptテストを、コードから確認できる事実に基づいて日本語で説明する。

## 調査手順

1. 指定されたテストファイルを全文読む。
2. import、`describe`、test case、hook、fixture、helper、test doubleを特定する。
3. テストが参照する本番moduleと、理解に必要な直接の実装だけを読む。
4. `package.json`とテストランナー設定を確認し、Vitest、Jest、Testing Library、MSW、Playwrightなどの前提を特定する。
5. リポジトリ内に仕様、ADR、テスト規約がある場合は、対象テストへ直接関係する箇所だけを読む。
6. テストをSmall、Medium、Largeのどれとして扱うか、実際のnetwork、filesystem、database、external serviceなどの依存範囲から判断する。Playwright、Browser Mode、MSWなどのtool名だけでsizeを上げず、リポジトリ固有の分類を優先する。

説明だけを求められた場合は、ファイルを変更せず、test、coverage、build、lintも実行しない。実行結果、修正、レビューを求められた場合だけ、その追加作業を行う。

## 説明の観点

### ファイル全体

- 何をテストするファイルか
- 対象となる公開契約とテスト層
- external dependency、fixture、mock、stub、fake、MSW handlerの有無
- `beforeEach`などで共有される準備とcleanup
- browser、DOM、network、timer、filesystemの使用範囲

共通setupで構成されている依存と、対象fileまたはcaseが実際に使用する依存を区別する。たとえばMSW workerが共通setupで起動していても対象caseがrequestを送らない場合は、その違いを明記する。

フロントエンドではcomponent、hook、provider、router、API boundary、E2Eのどこを検証しているかを示す。Node.jsではmodule、service、adapterなどの境界を示す。内部stateやDOM構造ではなく、利用側から観測できる振る舞いを中心に説明する。

### 各テストケース

テストごとに次を説明する。

1. テスト名を自然な日本語へ訳す。
2. 検証したい振る舞いを一文で述べる。
3. Arrange、Act、Assertへ分解する。
4. 各matcherが何を保証するかを説明する。
5. 失敗した場合に疑う契約違反を述べる。

`test.each`や`it.each`では、入力表、各parameterの意味、全caseで共通して保証する契約を説明する。`test.todo`、`test.skip`、`describe.skip`は未実装または未実行として扱い、成功済みと説明しない。

### TypeScriptテスト構文

使用されているものだけを説明する。

- `describe`: 関連する契約や状態のgrouping
- `test` / `it`: 1つの観測可能な振る舞い
- `test.each` / `it.each`: 複数データへ同じ契約を適用
- `beforeEach` / `afterEach` / `beforeAll` / `afterAll`: setup、共有範囲、cleanupのlifecycle
- `expect`とmatcher: 期待値と観測値の比較
- `vi.fn` / `jest.fn`、spy、module mock: test doubleと検証できる範囲
- `userEvent`: 利用者に近い入力やclick操作
- Testing Library query: role、accessible name、label、表示状態による観測
- MSW handler: requestをprocess内でinterceptするnetwork boundary
- fake timer: 時刻進行、timer cleanup、実時間との差
- Playwright fixture、locator、expect: browser context、操作対象、待機を含むE2E契約
- `async` / `await`: 非同期処理やuser interactionの完了を待つ理由

一般的なframework解説を長く書かず、対象コードでの役割に限定する。

## 出力形式

次の順で、必要な項目だけを簡潔に出力する。

```markdown
## 概要

## ファイルの構成

## テストケース

### `<test name>`

- 日本語訳:
- 目的:
- Arrange:
- Act:
- Assert:
- 保証する契約:

## テスト構文

## 本番コードとの関係
```

短いファイルでは見出しを減らし、説明がコード本体より過度に長くならないようにする。

## 正確性

- コード、仕様、実行結果を混同しない。
- コードから断定できない意図は「推測」と明記する。
- todo、skip、未実行のテストを成功済みとして扱わない。
- mockやspyの呼び出し検証を、利用者向けの最終結果と同一視しない。
- matcherが実際に検証していない振る舞いを保証済みと説明しない。
- `getByTestId`やCSS classの検証を、accessibilityや視覚品質の保証と同一視しない。
- MSWの利用だけで実network接続済みと断定せず、handlerが同一process内でinterceptする構成か確認する。
- testの不足や改善案は、ユーザーがreviewも求めた場合だけ提示する。
- 行番号を示す場合は、読み取った実ファイルの行番号を使用する。
