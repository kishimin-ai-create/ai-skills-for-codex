# Equivalent Mutants

## 判定条件

以下を説明できる場合のみ、Equivalent Mutant と判定する。

- 変更前の振る舞い
- 変更後の振る舞い
- 影響する入力領域
- すべての有効入力で、外部から観測可能な結果が同一になる理由

具体例だけで判断してはならない。

一部の入力で結果が同じであることは、Equivalent Mutant の根拠にならない。

## 禁止する判断

以下のような判断をしてはならない。

- 見た感じ同じ
- たぶん影響しない
- 実際には通らなそう
- 重要ではない
- テストを書くのが難しい
- Mutation Scoreへの影響が小さい

## 検証方法

必要に応じて、以下を使用して等価性を確認する。

- 追加テスト
- 小さな検証コード
- 入力領域の列挙
- 条件式の論理的な比較
- 型や制約による到達可能性の確認
- 外部から観測可能な出力の比較

検証のためにプロダクトコードを変更してはならない。

## 記録形式

Equivalent Mutant と判定した場合は、以下を記録する。

```text
Mutant ID:
File:
Line:
Mutation:
Classification: Equivalent
Original Behavior:
Mutated Behavior:
Affected Input Domain:
Reason:
Verification:
Evidence:
```

`Reason` には、すべての有効入力で外部から観測可能な結果が同一となる理由を記録する。

`Verification` には、判定に使用したテスト、検証コード、論理的な確認方法を記録する。

`Evidence` には、再確認可能な具体的な証拠を記録する。

## 判定できない場合

等価であることを説明できない場合は、Equivalent Mutant として扱ってはならない。

Test Gap、Product Code Smell、Product Bug、Tool Limitation、Flaky / Timeout のいずれかとして再分析する。
