---
name: remove-xunit-test-plan-comments
description: 指定されたC#のxUnitテストから、実装前の追跡用に残された`ID`、`Source`、`Given`、`When`、`Then`、`Error`、`Blocked by`、`Priority`形式の計画コメントだけを削除する。実装済みTests.csの冗長なテスト計画コメントを整理し、通常の理由コメントやSkip中の未実装計画を保護したいときに使用する。
---

# Remove xUnit Test Plan Comments

実装済みxUnitテストから、コードとテスト名が既に表現している計画コメントを削除する。コメント全般の一括削除は行わず、意味を持つ理由コメントと未実装のテスト計画を保護する。

## 対象コメント

テストメソッド内で、次のラベルから始まる連続した`//`コメントをテスト計画コメントとして扱う。

- `ID:`
- `Source:`
- `Given:`
- `When:`
- `Then:`
- `Error:`
- `Blocked by:`
- `Priority:`

ラベルの一部だけがある場合も、内容と位置から同じ計画ブロックだと確認できれば削除対象にする。ラベルを含まない通常コメントまで範囲を広げない。

## 保護するコメントとテスト

- 実装上の理由、採用しなかった方法、境界条件の理由を説明するコメントを残す。
- analyzer抑制、外部仕様の注意、既知の制約を説明するコメントを残す。
- `[Fact(Skip = ...)]`または`[Theory(Skip = ...)]`で、本文が計画コメントだけの未実装テストは変更しない。
- 計画コメントを消すと空のテストメソッドになる場合は削除せず、未実装計画として報告する。
- ユーザーがテストケース自体の削除を明示しない限り、メソッド、属性、テストデータ、assertionを削除しない。

## 手順

1. 対象ファイルと適用範囲の`AGENTS.md`、関連ADR、テスト規則を読む。
2. 対象ファイルを全文読み、各テストを実装済みまたは未実装のSkipに分類する。
3. `rg`で対象ラベルを検索し、削除候補を列挙する。
4. 各候補について、テスト名、入力、操作、assertionがコメントの内容を既に表現しているか確認する。
5. 実装済みテストの計画コメントだけを`apply_patch`で削除する。
6. 空行、属性、メソッド、テストデータ、実行コード、assertionが意図せず変わっていないか差分を確認する。
7. 対象テストを実行し、その後、変更リスクに応じて関連テストまたは全体テストを実行する。
8. リポジトリ規則が要求する場合は、意図したファイルだけをコミットする。pushは明示的に許可された場合だけ行う。

## 削除例

変更前:

```csharp
[Fact]
public void Subject_WhenCondition_ReturnsResult()
{
    // ID: SUBJECT-01
    // Source: docs/spec.md §1.
    // Given: a supported value
    // When: creation is requested
    // Then: creation succeeds
    // Error: none
    // Priority: High
    var result = Subject.Create("value");

    Assert.True(result.Succeeded);
}
```

変更後:

```csharp
[Fact]
public void Subject_WhenCondition_ReturnsResult()
{
    var result = Subject.Create("value");

    Assert.True(result.Succeeded);
}
```

## 完了条件

- 実装済みテストから対象ラベルの計画コメントが削除されている。
- 未実装のSkipテストと、理由を説明する通常コメントが維持されている。
- テストの属性、名前、入力、操作、assertionが変わっていない。
- 実行した検証と、保護した未実装計画を報告している。
