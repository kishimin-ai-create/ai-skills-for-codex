---
name: remove-typescript-test-plan-comments
description: 指定されたTypeScriptのVitest・Jestテストから、実装前の追跡用に残された`ID`、`Source`、`Given`、`When`、`Then`、`Error`、`Blocked by`、`Priority`形式の計画コメントだけを削除する。実装済みの.test.ts、.test.tsx、.spec.ts、.spec.tsxを整理し、通常の理由コメントやtest.todo・skip中の未実装計画を保護したいときに使用する。
---

# Remove TypeScript Test Plan Comments

実装済みTypeScriptテストから、コードとテスト名が既に表現している計画コメントを削除する。コメント全般の一括削除は行わず、意味を持つ理由コメントと未実装のテスト計画を保護する。

## 対象コメント

実装済みの`test`、`it`、`test.each`、`it.each`の直前にある、次のlabelから始まる連続した`//`コメントをテスト計画コメントとして扱う。

- `ID:`
- `Source:`
- `Given:`
- `When:`
- `Then:`
- `Error:`
- `Blocked by:`
- `Priority:`

labelの一部だけがある場合も、内容と位置から同じ計画blockだと確認できれば削除対象にする。labelを含まない通常コメントや、別のstatementに属するコメントまで範囲を広げない。

## 保護するコメントとテスト

- 実装上の理由、採用しなかった方法、境界条件の理由を説明するコメントを残す。
- ESLint抑制、外部仕様の注意、既知の制約を説明するコメントを残す。
- `test.todo`と`it.todo`の計画コメントを変更しない。
- `test.skip`、`it.skip`、`describe.skip`、`test.each(...).skip`など、実行対象外のテストに付随する計画コメントを変更しない。
- callbackが空、または計画コメントを消すと未実装であることが分からなくなるテストは削除せず、未実装計画として報告する。
- ユーザーがテストケース自体の削除を明示しない限り、`describe`、test case、parameter data、callback、expectationを削除しない。

## 手順

1. 対象ファイルと適用範囲の`AGENTS.md`、関連ADR、テスト規則を読む。
2. 対象ファイルを全文読み、各caseを実装済み、todo、skip、空callbackのどれかに分類する。
3. `rg`で対象labelと`test`・`it`宣言を検索し、削除候補との対応を列挙する。
4. 各候補について、test名、入力、操作、expectationがコメントの内容を既に表現しているか確認する。
5. 実装済みtestの直前にある計画コメントだけを`apply_patch`で削除する。
6. 空行、`describe`、test名、parameter data、callback、setup、test double、expectationが意図せず変わっていないか差分を確認する。
7. formatterを確認し、対象testを実行する。その後、変更riskに応じてtypecheck、lint、関連testまたは全体testを実行する。
8. リポジトリ規則が要求する場合は、意図したファイルだけをcommitする。pushは明示的に許可された場合だけ行う。

## 削除例

変更前:

```ts
// ID: SUBJECT-S-001
// Source: docs/spec.md §1
// Given: a supported value
// When: creation is requested
// Then: creation succeeds
// Priority: P0
test("creates a result for a supported value", () => {
  const result = createSubject("value");

  expect(result.succeeded).toBe(true);
});
```

変更後:

```ts
test("creates a result for a supported value", () => {
  const result = createSubject("value");

  expect(result.succeeded).toBe(true);
});
```

## 完了条件

- 実装済みtestから対象labelの計画コメントが削除されている。
- todo、skip、空callbackの未実装計画と、理由を説明する通常コメントが維持されている。
- `describe`、test名、parameter data、callback、setup、test double、expectationが変わっていない。
- 実行した検証と、保護した未実装計画を報告している。
