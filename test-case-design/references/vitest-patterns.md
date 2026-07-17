# Vitest/Jest Patterns

## Outline

```ts
describe("対象の公開契約", () => {
  // 境界条件と期待する振る舞いをtodo名で仕様化する。
  test.todo("入力が有効な時、登録結果を返すこと");
  test.todo("入力が不正な時、永続化せず検証エラーを返すこと");
});
```

todo名は実装詳細ではなく、入力条件・観測結果・不変条件を含める。

## Implemented test

```ts
test("入力が有効な時、登録結果を返すこと", async () => {
  // Arrange
  const input = createValidInput();

  // Act
  const result = await execute(input);

  // Assert
  expect(result).toMatchObject({ status: "success" });
});
```

共有前提は適切なbeforeEachへ置き、テスト固有の追加条件はケース内で構築する。クリーンアップは利用中のランナーが提供する終了フックを確認して登録する。

## Failure handling

- 実装と期待が一致しない場合は、仕様・テスト・実装のどれが誤っているかを切り分ける。
- 仕様不明でのskipは、理由、影響、確認者、再開条件を残す。
