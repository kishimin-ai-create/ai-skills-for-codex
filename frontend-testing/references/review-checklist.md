# Frontend Testing Review Checklist

## 計画

- [ ] 公開契約、ユーザー行動、データ不変条件、リスクを記録した
- [ ] Unit、Component/Integration、E2E、A11yの責務を分けた
- [ ] 既存のテスト設定、test-utils、CI、ADRを確認した

## 実装

- [ ] AAAと1ケース1目的を守った
- [ ] セマンティッククエリを優先し、TestIdの理由をコメントした
- [ ] 内部stateや実装詳細に依存していない
- [ ] Snapshotを小さく限定した

## 境界回帰

- [ ] ProxyのHeader・Body・Status・画面表示を検証した
- [ ] Runtime Config、Auth lifecycle、Timestamp、Pagination、Loading、i18nを必要な範囲で検証した
- [ ] A11y自動検査と手動確認を組み合わせた

## CIと報告

- [ ] 型検査、Lint、Formatter、テストの実行コマンドを記録した
- [ ] 失敗をテスト・実装・環境・仕様不明に分類した
- [ ] フレーク、未実装、skip、残存リスク、手動確認を報告した
