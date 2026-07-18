---
name: eslint-custom-rules
description: プロジェクトにおけるカスタムESLintルールの設計および運用ガイドライン。
---

# Custom ESLint Rules

## When to Write a Custom Rule

- 同じレビューコメントが複数のPRで繰り返される場合は、ESLintルールとして自動化する（ボーイスカウト・ルール）。
- 型チェックではチーム固有のルールを表現できない場合（例：すべての画面で権限チェック用Componentの使用を必須とするなど）。
- 制約が決定的であり、正しい答えが1つに定まる場合。

## Rules for Writing Rules

- 修正内容が決定的な場合は、自動修正（Auto Fix）を実装し、CIで自動適用できるようにする。

- すべての `eslint-disable` 行には理由コメントを必須とし、理由のない無効化は認めない。

  ```js
  // Bad
  // eslint-disable-next-line @typescript-eslint/no-explicit-any

  // Good
  // eslint-disable-next-line @typescript-eslint/no-explicit-any -- external SDK type is untyped
  ```

- 1つのルールは1つの制約だけを扱うようにし、複数のチェックを1つのルールへまとめない。

## CI Integration

- 自動修正可能なルールは、BuildをFailさせるのではなく、CIで自動修正を実行し、その修正をCommitする運用とする。
- BuildをFailさせるルールは、自動修正できない重大な制約に限定する。
