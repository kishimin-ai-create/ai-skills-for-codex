# Quality Gates

## 許容しない状態

以下の状態を許容しない。

- SURVIVED
- LIVED
- NO COVERAGE
- NOT COVERED
- TIMEOUT
- TEST ERROR
- 実行結果不明
- 原因未調査
- 推測による放置

すべてのミュータントを個別に確認する。

## 許容される最終状態

最終的に許容されるミュータントは以下のみとする。

- KILLED
- Equivalent Mutant
- Tool Limitation として再現可能な証拠があるもの

以下を終了理由として認めない。

- Mutation Score が十分高い
- 重要ではないコードだから
- テストを書くのが難しい

## 品質指標

Raw Mutation Score は品質指標として使用しない。

Mutation Score が 100% 未満の場合、生存しているすべてのミュータントについて分類と根拠を記録する。

品質指標には Effective Mutation Score を使用する。

```text
Effective Mutation Score =
Killed / (Killed + Actionable Survived)
```

Required:

```text
100%
```

## 完了条件

以下をすべて満たすこと。

```text
Actionable Survived Mutants = 0
Unclassified Mutants = 0
Not Covered Mutants = 0
Uninvestigated Timeouts = 0
Effective Mutation Score = 100%
```

Raw Mutation Score は完了条件としない。
