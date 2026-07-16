# Timeouts and Tool Errors

## Timeout Investigation

TIMEOUT を成功として扱ってはならない。

以下を確認する。

- baseline test duration
- mutation test timeout
- timeout coefficient
- worker count
- parallelism
- 対象テスト
- 対象ミュータント

ミュータントによって無限ループ、極端な処理時間の増加、停止条件の消失が発生していないか確認する。

## Flaky Test

既存テストが不安定である可能性がある場合は、同一テストスイートを複数回実行する。

実行結果が安定しない場合は、Flaky として記録する。

Flaky な状態を放置したまま Mutation Test の結果を確定してはならない。

## Test Error

TEST ERROR が発生した場合は、以下を確認する。

- テストコードのエラー
- テスト環境の不備
- 依存サービスの状態
- Fixture や Helper の不整合
- Mutation Tool とテストフレームワークの互換性
- 対象ミュータントによる初期化失敗
- 実行コマンドや設定の誤り

原因を特定できない状態で放置してはならない。

## Tool Limitation

ツール由来の無効なミュータントと判断する場合は、再現可能な証拠を記録する。

以下を確認する。

- 同一条件で再現するか
- 対象ツールや Mutator 固有の制約か
- テストコードやプロダクトコードに原因がないか
- 設定によって結果が変化するか
- ツールの出力やログから原因を確認できるか

推測だけで Tool Limitation と分類してはならない。

## Configuration Changes

Timeout や Tool Error の調査で設定を変更した場合は、変更理由を記録する。

対象例:

- timeout
- timeout coefficient
- worker count
- concurrency
- parallelism
- test runner options
- mutation tool options

スコア向上や未調査結果の除外だけを目的として設定を変更してはならない。

## Record Format

TIMEOUT、Flaky、TEST ERROR、Tool Limitation は以下の形式で記録する。

```text
Mutant ID:
File:
Line:
Status:
Classification:
Baseline Duration:
Mutated Duration:
Configuration:
Investigation:
Reproduction Steps:
Cause:
Evidence:
Resolution:
Remaining Risk:
```

設定を変更した場合は、以下も記録する。

```text
Setting:
Previous Value:
New Value:
Reason:
Observed Effect:
```

## Unresolved Results

原因を特定できない場合は、未解決として明示する。

以下の状態で完了してはならない。

- 未調査の TIMEOUT が存在する
- 原因不明の TEST ERROR が存在する
- 根拠のない Tool Limitation が存在する
- Flaky の再現条件が記録されていない
