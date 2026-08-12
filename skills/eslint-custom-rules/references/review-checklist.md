# ESLintルールレビュー・完了チェックリスト

- [ ] 規約と違反・許可例が文章とテストで一致している
- [ ] 既存rule、型検査、formatterでは代替できない理由がある
- [ ] parser、JSX、TypeScript、scope、aliasの前提を確認した
- [ ] valid/invalid、境界、複数違反、fix outputをRuleTesterで検証した
- [ ] false positive、重複report、無限fix、コメント破壊がない
- [ ] flat/legacy config、export、severity、ignoreを確認した
- [ ] warningからerrorへの移行と既存違反の扱いを記録した
- [ ] disableには理由・範囲・期限またはissueがある
- [ ] 型検査、rule test、全体Lint、buildの結果を記録した
- [ ] 変更対象、owner、ロールバック、残存リスクを報告した
