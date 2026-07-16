# Test Design

## Test Gap

不足している振る舞いだけを検証するテストを追加する。

ミュータントだけを殺すための不自然なテストを書いてはならない。

テストはプロダクトの仕様を表現すること。

テスト追加は次の順で検討する。

1. 既存のテーブル駆動テストへケースを追加する。
2. 既存の Parameterized Test へケースを追加する。
3. 既存テストへ Assertion を追加する。
4. 既存テストの入力を改善する。
5. 新しいテストケースを追加する。

新しいテストケースの追加は最後の手段とする。

## Test Data

容易な入力だけを使用してはならない。

対象仕様に応じて、必要なケースを選択する。

候補

- 正常値
- 最小値
- 最大値
- 境界値直前
- 境界値
- 境界値直後
- 0
- 負数
- 空文字
- 空配列
- null
- undefined
- 重複
- 未知値
- 不正値
- 非常に長い値
- locale違い

選択した理由を説明できること。

## Assertions

弱い Assertion を使用してはならない。

悪い例

```text
expect(result).toBeDefined()
expect(result).toBeTruthy()
expect(array.length).toBeGreaterThan(0)
```

対象の仕様を確認できる場合は、具体的な値を検証する。

例

```text
expect(result).toEqual(expected)
expect(result.status).toBe("published")
expect(result.locale).toBe("ja")
```

部分一致を使用する場合は、完全一致を使用しない理由を説明できること。

## Snapshot Test

Snapshot Test のみでミュータントを検出しようとしてはならない。

Snapshot の更新だけでテストを成功させてはならない。

Snapshot が変更された場合は、差分を確認する。

期待仕様の変更であることを説明できない Snapshot の更新は禁止する。

## Mock

過剰な Mock によってプロダクトコードの振る舞いを再実装してはならない。

次の内容だけを確認するテストは原則として使用しない。

```text
mock called
mock called once
mock called with
```

呼び出し自体が仕様である場合を除き、外部から観測可能な結果を検証する。

## AI Rules

AI は Mutation Report を最初に読む。

Report を読まずにテストを追加してはならない。

次の順序を守る。

```text
Report
↓
Mutant
↓
Production Code
↓
Existing Test
↓
Missing Behavior
↓
Test Case
```

追加した各テストケースについて、次を記録する。

```text
Test Case:
Target Mutant:
Why it survived:
Why this case kills it:
```
