# Mutant Analysis

## 分析手順

各 SURVIVED ミュータントについて、次の手順で分析する。

1. 変更前のコードを確認する。
2. ミュータントによる変更内容を確認する。
3. 変更前と変更後の意味的な差異を説明する。
4. 差異が発生する入力条件を特定する。
5. 現在のテストが差異を検出できなかった理由を説明する。
6. 次のいずれかに分類する。
   - Test Gap
   - Equivalent Mutant
   - Product Code Smell
   - Product Bug
   - Tool Limitation
   - Flaky / Timeout

分類不能は禁止する。

## Test Gap

不足している振る舞いを特定する。

その振る舞いだけを検証する最小のテストを追加する。

テストは仕様を表現するものとし、ミュータントだけを殺す不自然なテストを書いてはならない。

テスト追加は次の順で検討する。

1. テーブル駆動テストへのケース追加
2. Parameterized Testへのケース追加
3. Assertionの追加
4. テスト入力の改善
5. 新規テストケースの追加

## Equivalent Mutant

以下を説明できる場合のみ Equivalent Mutant とする。

- 変更前の振る舞い
- 変更後の振る舞い
- 影響する入力領域
- すべての有効入力で外部から観測可能な結果が同一となる理由

次の判断をしてはならない。

- 見た感じ同じ
- たぶん影響しない

必要に応じて追加テストまたは検証コードで確認する。

以下を記録する。

```text
Mutant ID:
File:
Line:
Mutation:
Classification: Equivalent
Reason:
Verification:
```

## Product Code Smell

原因がテスト不足ではなく、プロダクトコードの構造にある場合に分類する。

例

- 到達不能コード
- 意味のない条件
- 不要な分岐
- 重複処理
- 常に同じ結果となる条件
- 削除しても振る舞いが変わらない処理

コードは変更せず、次を報告する。

```text
Classification: Product Code Smell

対象:
問題:
生存した理由:
推奨対応:
```

## Product Bug

プロダクトコードの不具合を発見した場合に分類する。

テストを不具合に合わせて変更してはならない。

プロダクトコードを変更してはならない。

作業を停止し、次を報告する。

```text
Classification: Product Bug

対象コード:
期待される振る舞い:
現在の振る舞い:
再現条件:
関連ミュータント:
推奨対応:
```

## Tool Limitation

ミューテーションツールの制約であることを再現可能な証拠とともに記録する。

## Flaky / Timeout

次を調査する。

- baseline test duration
- mutation test timeout
- timeout coefficient
- worker count
- parallelism
- 対象テスト
- 対象ミュータント

ミュータントによる無限ループ等の可能性も確認する。

設定を変更した場合は、その理由を記録する。
