---
name: test-patterns
description: Unit、Component、Integration、API、E2Eテストで再利用できる実装パターン、モック境界、非同期検証、失敗診断を選択するときに使用する。
---

# Test Patterns

テスト対象の公開契約を最優先し、プロジェクトの既存ランナー・命名・fixture・コマンドに合わせてパターンを適用する。

## パターン選択

- 純粋関数：代表値と境界値を表形式でparameterizeする。
- UI：role、label、visible textなど利用者向けクエリで操作し、状態遷移とイベントを検証する。
- 非同期：成功、loading、empty、error、retry、cancel、raceを決定的な待機で検証する。
- HTTP：実ネットワークではなく境界をモックし、statusだけでなくheader・body・schemaを検証する。
- 時刻・乱数・UUID：テスト内で固定し、終了時に復元する。
- DB：fixtureを最小化し、トランザクション・cleanup・一意性を明示する。
- E2E：ユーザージャーニー、認証境界、主要な失敗経路に限定し、低層テストと重複させない。

## 禁止事項

- 実装詳細だけを検証するセレクターやprivate関数への依存
- グローバル状態・実時刻・外部APIへの無制御依存
- 失敗を隠す無条件retry、sleep、snapshot更新
- fixtureの共有変更、テスト順序依存、秘密情報の埋め込み

## 実施

1. 期待する振る舞いをテスト名に書く。
2. Arrange、Act、Assertを分け、1テストの主張を明確にする。
3. mockは最も外側の境界に置き、契約違反レスポンスも用意する。
4. 失敗時に診断できるメッセージ、trace、fixture識別子を残す。
5. プロジェクトの既存規約を必要時のみ参照する。
