# Frontend Testing

LintからE2E、アクセシビリティテストまで、フロントエンドコードの自動品質チェックを計画する際に、このスキルを使用する。

## Static Analysis First

静的解析は、任意の後処理ではなく、標準の開発フローに含める。

### Why it matters

- 品質を守る
- コードスタイルを統一する
- 開発ルールを明確にする
- 自動化によって人的ミスを減らす
- CIやPRの品質ゲートへ自然に統合できる

## Static Analysis Tooling

| Category          | Purpose                              | Typical tools                                |
| ----------------- | ------------------------------------ | -------------------------------------------- |
| **Type checking** | 型に起因するBugを防ぐ                | TypeScript                                   |
| **Linting**       | コードや設定のルールを適用する       | ESLint、Biome、Stylelint                     |
| **Formatting**    | 差分を小さく保ち、スタイルを統一する | Prettier、Biome                              |
| **Support tools** | コード品質の自動化や調査を行う       | lint-staged、lefthook、knip、depcheck、madge |

## Static Analysis Rollout

- プロジェクトのできるだけ早い段階で静的解析を導入する。
- 既存プロジェクトでは段階的に導入する。
- 広く利用されている基本ルールセットを優先し、必要最小限の調整を行う。
- プロジェクトやチームの変化に合わせて、ルールを定期的に見直す。

### When adding new lint rules mid-project

- 一括で自動修正できるものは、まとめて修正する。
- 未対応箇所が多すぎる場合は、まず新規または変更したコードだけにルールを適用する。
- 調整なしに開発計画を壊すような、突然のルール追加は避ける。
- コード品質の向上と開発者体験のバランスを取る。

## Testing Philosophy

- 壊れやすい実装詳細のUnit testへ過度に投資しない
- ユーザーの振る舞いを反映するComponent / Integration testを重視する
- E2Eは最も重要なユーザーフローへ限定して使用する

## Tool Recommendations

| Layer                       | Tooling                                        | What to test                                                      |
| --------------------------- | ---------------------------------------------- | ----------------------------------------------------------------- |
| **Unit**                    | `vitest`                                       | 純粋なビジネスロジック、Utility、独立した計算処理                 |
| **Component / integration** | `React Testing Library`、`Vue Testing Library` | 描画、操作、UI状態の変化、Component間の連携                       |
| **E2E**                     | `Playwright`                                   | ページをまたぐFlow、Routing、Pagination、重要なユーザージャーニー |
| **A11y automation**         | Component / E2E testと組み合わせた `axe-core`  | 構造的なアクセシビリティ問題                                      |

## What to Test Where

| Concern                            | Unit       | Component / Integration         | E2E                                | Manual     |
| ---------------------------------- | ---------- | ------------------------------- | ---------------------------------- | ---------- |
| Pure business logic                | Yes        | UI経由で確認する場合もある      | ほとんど行わない                   | No         |
| Hooks / internal state logic       | 場合による | 利用するComponent経由を優先する | ほとんど行わない                   | No         |
| UI interaction and visible changes | No         | Yes                             | 場合による                         | 場合による |
| Cross-component coordination       | No         | Yes                             | 場合による                         | 場合による |
| Route transitions / page flows     | No         | 限定的                          | Yes                                | 場合による |
| API fetch/update flow              | 場合による | Mockを使用して確認する          | Backendとの連携が重要なFlowではYes | 場合による |
| Critical user journeys             | No         | 場合による                      | Yes                                | 場合による |
| Screen reader behavior             | No         | 限定的                          | 限定的                             | Yes        |
| Keyboard navigation                | 場合による | Yes                             | Yes                                | Yes        |

## Unit Test Guidance

- 外部I/Oを持たないFunctionを中心にテストする。
- ビジネスロジックをHooks、Composables、Moduleへ抽出し、テスト可能な状態を保つ。
- ユーザーへの影響なしに変更できる実装詳細をテストしない。

## Component / Integration Test Guidance

- **ユーザーの視点**からテストする。
- 実装方法ではなく、UIが何をするかを検証する。
- 内部Stateを直接確認するより、描画と操作を通じた検証を優先する。
- 外部ServiceのMockは必要な場合のみ使用する。

```ts
// Good direction:
// click button -> visible text changes from X to Y
// Avoid: inspect internal component state directly
```

## E2E Test Guidance

一連の振る舞い全体を検証する必要がある場合にのみ、E2Eを使用する。

### Good candidates

- 重要な業務フロー
- 多数のAPI Callと状態遷移を含む複雑なページ
- Paginationや複数ページ間のNavigationを含むFlow
- 機能の組み合わせによって壊れやすいScenario

### Avoid

- Unit testやComponent testですでに十分な信頼性を得られている振る舞いを、重複して確認すること
- 影響の小さいUI詳細に対して、大規模なE2E Suiteを作成すること

## Runtime Boundary Regression Tests

Browser、Server、Proxy、Deploymentの境界をまたぐフロントエンドのBugに対しては、対象を絞ったRegression testを追加する。

- **API proxy bugs**：Backend相当のHeaderとBodyを使ってProxy Functionをテストする。Statusが200であることだけでなく、Response BodyをParseできることも検証する。
- **Deployment URL bugs**：BackendのRuntime Configが、Frontend Requestと同一OriginのBackend URLを拒否することをテストする。
- **Rendered data bugs**：API / Proxy Testに加えて、返されたRecordが画面に表示され、Empty stateが表示されないことをComponentまたはBrowser Testで確認する。
- **Auth lifecycle bugs**：Storage用Helperを直接確認するだけでなく、表示されるUIを通してLogin時の保存とLogout時の削除をテストする。
- **Timestamp bugs**：既知のUTC Timestampに対して描画されるTextを検証する。期待するTimezoneをTest名と実装の両方で明示する。
- **Pagination bugs**：Next / PreviousをクリックするとQuery Parameterが変わること、Filter変更時にPageが `1` へ戻ることをテストする。
- **Full-page loading bugs**：初回Loadingでは `role="status"` と、アプリで使用するBrand付きFull-page ClassまたはLandmarkをテストする。ページを操作可能なままにするScoped refetch loadingは別にテストする。
- **i18n loading bugs**：デフォルト以外のLocaleでLoading stateを描画し、表示されるLoading TextとLogoのalt Textを検証する。Browser TitleやApp Shell Titleがある場合は、それらもLocaleに応じて変わることを確認する。

## Accessibility Testing

- 自動テストと手動確認を組み合わせる。
- 広範囲の問題を低コストで検出するために `axe-core` を使用する。
- 100%の自動化Coverageを目指さない。
- 次の項目は手動で確認する。
  - Screen readerの操作フロー
  - KeyboardのみでのNavigation
  - Focusの挙動
  - Error messageの使いやすさ

## CI and Team Workflow

- CIで静的解析を自動実行する。
- ルールが十分に成熟している場合は、品質チェック失敗時にMergeをBlockingする。
- Tool設定を理解しやすく、保守しやすい状態に保つ。
- ルールを単なる制約ではなく、開発を支援する仕組みとして理解できるよう、その目的を文書化する。
