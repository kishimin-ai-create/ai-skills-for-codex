# Playwright fixtures

Playwright fixtureを使って、テストごとに分離された準備処理と依存オブジェクトを型安全に提供する。公式仕様は[Overriding fixtures](https://playwright.dev/docs/test-fixtures#overriding-fixtures)を参照する。

## 選択基準

- 複数のspecで再利用する準備、後片付け、Page Objectの生成をfixtureへ置く。
- シナリオ固有の操作とassertionはspecへ残す。
- fixtureは要求されたテストだけで生成される性質を利用し、巨大な共通`beforeEach`を避ける。
- 標準のスコープはtestとする。安全に共有でき、構築コストが高い資源だけをworker scopeの候補にする。
- built-in fixtureの上書きは、対象の全テストに共通する契約だけに限定する。

## 型付きPOM fixture

基底の`test`を拡張し、Page Objectを同じテストスコープの`page`から生成する。specはこのモジュールから`test`と`expect`を読み込む。

```ts
import { expect, test as base } from "@playwright/test";
import { LoginPage } from "../pages/login-page";

type Fixtures = {
  loginPage: LoginPage;
};

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, provide) => {
    await provide(new LoginPage(page));
  },
});

export { expect };
```

fixtureコールバックの第2引数は位置で決まるため、名前は`use`に限定されない。React Hooks向けのLint規則が`use`をHookと誤認する構成では、`provide`など責務が伝わる名前を使う。

## built-in fixtureの上書き

`base.extend()`では`page`などのbuilt-in fixtureも上書きできる。依存fixtureを引数から受け取り、準備後に元の値を提供する。

```ts
import { test as base } from "@playwright/test";

export const test = base.extend({
  page: async ({ baseURL, page }, provide) => {
    if (baseURL === undefined) {
      throw new Error("playwright.config.tsでbaseURLを設定してください");
    }

    await page.goto(baseURL);
    await provide(page);
  },
});
```

- `baseURL`は`playwright.config.*`または`test.use()`から与え、URLをfixtureへハードコードしない。
- 上書きした`page`に依存するPOMは、同じブラウザーコンテキストとページを共有する。
- cleanupが必要なら`await provide(value)`の後に置く。提供前がsetup、提供後がteardownになる。
- specが`@playwright/test`から直接`test`をimportすると独自fixtureは使われない。fixtureモジュールを唯一のimport境界にする。

## 初期化順序

自動遷移する`page` fixtureは便利だが、最初のnavigationより前に必要な初期化と競合しうる。

- 時計、乱数、feature flag、認証用init scriptなどをnavigation前に設定するテストがあるか確認する。
- 全テストが同じ遷移を必要としないなら、`page`を上書きせず、専用fixtureまたは明示的なPOM操作にする。
- VRTで時刻や乱数を固定する場合は、init script適用後に明示的に再遷移し、基準画像と比較画像の順序を一致させる。
- fixture同士の依存を引数で宣言し、暗黙の実行順や別fixtureの副作用へ依存しない。

## レビュー項目

- fixtureの型がspecへ伝播している。
- fixtureはPOMの生成と提供に集中し、利用者シナリオを隠していない。
- テストごとの`page`分離を維持し、不要なcontextやpageを追加生成していない。
- 上書きしたbuilt-in fixtureの副作用が、そのfixtureを使う全テストで妥当である。
- setup失敗時のエラーが、欠けた設定や前提を特定できる。
- custom fixtureを使うspecが、独自の`test`と`expect`を正しいモジュールからimportしている。
