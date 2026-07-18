# Storybookレビュー・完了チェックリスト

- [ ] CSF 3.0のMeta/StoryObjが型検査され、公開APIとStory名が一致している
- [ ] Default、Loading、Empty、Error、Disabled、Validation、境界値を必要に応じて網羅している
- [ ] decorators/providersが最小限で、Story専用の本番分岐がない
- [ ] playはrole/labelなどの利用者向けクエリを使い、操作結果をexpectで検証している
- [ ] MSWで成功・空・遅延・4xx/5xx・再試行・キャンセルを再現できる
- [ ] axeとキーボード、フォーカス、名前・説明、コントラストを確認している
- [ ] mobile/desktop、theme、RTL、長文、縮小モーションの要否を判断している
- [ ] Visual Regressionの日時・乱数・フォント・アニメーションが固定されている
- [ ] build、interaction、a11y、Visual RegressionのCI結果と失敗成果物を確認した
- [ ] 実行コマンド、差分理由、残存リスク、未実施の手動確認を報告した
