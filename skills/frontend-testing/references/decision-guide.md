# Frontend Testing Decision Guide

## 層の選び方

- 純粋な計算・変換・バリデーションはUnit。
- 表示、操作、UI状態、コンポーネント連携はComponent/Integration。
- Routing、複数API、主要業務フローはE2E。
- 構造的なA11yはaxe-core、読上げ・キーボード・フォーカス・文言は手動確認。

## Mockの判断

- 依存境界の小さなfake/stubはUnitで許可する。
- API契約、DB状態、トランザクション、外部HTTPを検証するIntegrationでは、テストDB・コンテナ・契約サーバーを優先する。
- Mockで隠れる不変条件、Header、Body、認可、タイムアウトがないかを確認する。

## 品質ゲート

- 変更範囲に対する型検査、Lint、Formatterを先に実行する。
- 変更されたUnit/Component/Integrationから始め、次に重要E2EとA11yを実行する。
- 実行時間、フレーク、失敗原因、再試行回数を記録し、Merge Blockingの範囲を段階的に決める。

## 採用を見送る条件

- 実装詳細を固定するためだけの大量Unit test。
- 低リスクUIを全てE2Eで重複検証する。
- axeの成功だけでA11y完了と判断する。
- statusだけを確認してProxyやAPIのBody・表示を確認しない。
