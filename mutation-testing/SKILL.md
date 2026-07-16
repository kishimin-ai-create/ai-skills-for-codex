---
name: mutation-testing
description: ミューテーションテストを実施し、生存ミュータントを分析・分類しながらテストスイートを改善する。
---

# Mutation Testing

## 目的

ミューテーションテストによって、テストスイートが実際に誤りを検出できることを確認する。
Mutation Score を目的としてはならない。
殺害可能なミュータントをすべて検出できるテストスイートを構築することを目的とする。

## 手順

1. プロジェクト構成、テストフレームワーク、ミューテーションテストツールを確認する。
2. 通常テストを実行し、すべて成功することを確認する。
3. コードカバレッジを取得する。
4. Mutation Report を取得する。
5. Report をもとに各ミュータントを個別に分析・分類する。
6. Test Gap の場合は不足している振る舞いを検証するテストを追加する。
7. 通常テストを実行する。
8. Mutation Test を再実行する。
9. Actionable Survived Mutants が 0 になるまで繰り返す。
10. 最終レポートを作成する。

## 完了条件

- 通常テストが成功している。
- Mutation Test を再実行している。
- Actionable Survived Mutants = 0
- Unclassified Mutants = 0
- Not Covered Mutants = 0
- 未調査の Timeout が存在しない。
- Equivalent Mutant の根拠を記録している。
- 追加したテストと対象ミュータントの対応を記録している。
- Effective Mutation Score = 100%
- 最終レポートを作成している。
