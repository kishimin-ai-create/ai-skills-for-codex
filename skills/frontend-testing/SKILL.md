---
name: frontend-testing
description: フロントエンドの静的解析、Unit、Component/Integration、E2E、アクセシビリティ、Runtime境界回帰、CI品質ゲートを計画・実装・レビューするときに使用する。
---

# Frontend Testing

テストは実装詳細ではなく、利用者が観測する振る舞い、公開契約、データ不変条件を表す。静的解析からE2Eまでをリスクと実行コストで層別化し、同じ保証を重複させない。

## テスト計画ワークフロー

### 1. 品質基準と実行環境を確認する

- package scripts、テスト設定、TypeScript、ESLint/Biome、Formatter、CI、既存test-utilsを確認する。
- 対象ブラウザ、Node、DB、HTTP、Proxy、Deployment、認証、i18n、アクセシビリティ環境を一覧化する。
- 既存のADR、AGENTS.md、プロジェクト固有の品質ゲートを優先する。

### 2. 静的解析を最初に置く

- TypeScript型検査、Lint、Formatterを標準フローへ組み込む。
- lint-staged、lefthook、knip、depcheck、madgeなどは課題と費用を確認して必要な範囲で使う。
- 新規ルールは段階導入し、既存プロジェクトでは変更箇所または新規コードから適用する。
- 自動修正可能な差分を先に処理し、ルール追加で開発計画を突然破壊しない。

### 3. テスト層を選ぶ

- Unit: 外部I/Oを持たない純粋関数、Utility、計算、状態変換。
- Component/Integration: ユーザー操作、描画、UI状態、コンポーネント間連携、外部サービス境界。
- E2E: ルート遷移、複数API、重要な業務フロー、壊れやすいユーザージャーニー。
- A11y: axe-core自動検査と、スクリーンリーダー・キーボード・フォーカス・エラー文言の手動確認。
- 添付の詳細な層別表は[attached-quality-plan.md](./references/attached-quality-plan.md)を読む。

### 4. 利用者の振る舞いを検証する

- Component/Integrationではロール、名前、ラベル、表示テキスト、操作結果などセマンティッククエリを優先する。
- 内部state、Hook呼び出し、実装クラス、DOM構造の細部を直接検査しない。
- getByTestIdは他の意味のあるクエリが使えない理由をコメントし、最後の手段にする。
- Arrange、Act、Assertを分け、1ケース1つの主要な振る舞いを検証する。
- スナップショットは小さく対象を限定し、更新だけで仕様差分を隠さない。

### 5. Runtime境界の回帰を追加する

- API ProxyはStatusだけでなく、Backend相当のHeader・Bodyを解析して表示まで確認する。
- Runtime ConfigはFrontendと同一OriginになるBackend URLを拒否することを検証する。
- API/Proxyのレコードが画面に表示され、空状態へ誤遷移しないことをComponentまたはBrowser testで確認する。
- 認証StorageのHelperだけでなく、Login時の保存とLogout時の削除をUI経由で検証する。
- UTC Timestampは期待Timezoneをテスト名と実装で明示する。
- PaginationはNext/PreviousでQuery Parameterが変わり、Filter変更時にPageが1へ戻ることを検証する。
- 初回Full-page loadingとScoped refetch loadingを分け、role=status、ブランド表示、操作可能性を確認する。
- 非デフォルトLocaleのLoading、Logo alt、Browser/App Shell titleを検証する。

### 6. CIと品質ゲートを運用する

- 静的解析、Unit、Component/Integration、E2E、A11yを適切な並列性と実行時間でCIへ組み込む。
- 成熟したチェックは失敗時にMergeをBlockingし、目的・修正方法・例外申請を文書化する。
- 失敗時はテスト、実装、環境、仕様不明を分類し、無言のskipを残さない。

## テスト層の選択基準

- Unitは高速な計算・変換に限定し、壊れやすい実装詳細へ過度に投資しない。
- Component/Integrationを中心に、ユーザー視点のUI契約を検証する。
- E2Eは重要なフローへ限定し、下位層と同じ分岐を重複させない。
- 外部ServiceのMockは必要な境界に限定し、実DB・契約サーバー・テスト環境が必要な契約を内部Mockだけで代替しない。

## アクセシビリティの基準

- axe-coreを広範な低コスト検出に使うが、自動化100%を目標にしない。
- Screen reader、キーボードのみ、フォーカス移動、エラー文言、ズーム、コントラストを手動確認する。
- A11yテストはComponent/E2Eと組み合わせ、重要なユーザーフローに組み込む。

## 参照資料を選ぶ

- 添付内容の全文、ツール表、テスト層表、Runtime境界回帰、CI方針は[attached-quality-plan.md](./references/attached-quality-plan.md)を読む。
- 既存Skillの命名、AAA、セマンティッククエリ、snapshot規則は[testing-rules-catalog.md](./references/testing-rules-catalog.md)を読む。
- テスト設計と実装の完了条件は[review-checklist.md](./references/review-checklist.md)を読む。

## 出力契約

テスト計画または変更結果と併せて、次を報告する。

1. 対象契約、リスク、テスト層、選択理由
2. 静的解析、Unit、Component/Integration、E2E、A11yの対象
3. Runtime境界、i18n、Pagination、Loading、Authの回帰項目
4. 実行コマンド、品質ゲート、失敗分類、未実装項目
5. 残存リスク、手動確認、ロールバック、追加確認事項
