# Vitest/Jest Patterns

## Outline

```ts
describe("対象の公開契約", () => {
  // ID: REGISTRATION-S-001
  // Source: requirements.md §3 "Registration"
  // Given: 登録可能な入力が指定されている
  // When: 登録を実行する
  // Then: 登録結果を返し、同じ副作用を重複して発生させない
  // Blocked by: 登録処理の実装
  // Priority: P0
  test.todo("入力が有効な時、登録結果を返すこと");

  // ID: REGISTRATION-S-002
  // Source: requirements.md §3 "Validation"
  // Given: 必須値が欠けた入力が指定されている
  // When: 登録を実行する
  // Then: 永続化せず、利用者が修正可能な検証エラーを返す
  // Error: required
  // Priority: P0
  test.todo("入力が不正な時、永続化せず検証エラーを返すこと");
});
```

各計画コメントは対応する`test.todo`の直前へ置く。todo名は実装詳細ではなく、入力条件・観測結果・不変条件を含める。

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
