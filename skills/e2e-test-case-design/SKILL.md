---
name: e2e-test-case-design
description: Design assertion-free Playwright E2E test scaffolds from user journeys, API contracts, and UI requirements without adding fixtures, mocks, or production implementation.
---

# E2E Test Case Design

PlaywrightによるE2Eテストを、実装前に検討・追跡できる未実装テストの足場へ変換する。生成するのは、ユーザー操作と観測可能な結果を表すテスト名と計画コメントだけであり、assertion、fixture、mock、stub、test data、プロダクションコードは追加しない。

## 適用範囲

- 要件、画面仕様、API契約、ルーティング、既存E2Eテストから、ブラウザ上のユーザージャーニーを設計するときに使用する。
- `test-case-design`の振る舞い中心のケース設計と、`xunit-aspnet-core-test-case-design`の未実装・計画コメントの形式をPlaywrightへ適用する。
- E2Eはテストの目的を表す層であり、サイズではない。Small／Medium／Largeは実際の依存境界で個別に決める。

## 開始前に確認すること

1. リポジトリの`AGENTS.md`、関連ADR、実装計画、UI仕様、API仕様を読む。
2. `package.json`、`playwright.config.*`、`testDir`、`projects`、`webServer`、既存のfixture・global setup・認証設定を確認する。
3. 実際に接続するサービスを列挙する。Frontendだけか、localhost APIか、デプロイ済みAPIか、外部サービスかを区別する。
4. 既存のUnit／Component／Integration／Contractテストで既に証明されている観測を確認し、同じassertionを無目的にE2Eへ複製しない。

## サイズ判定

`test-sizes`とリポジトリ固有ADRを優先する。Playwrightを使うこと自体はサイズの根拠にしない。

| 依存 | サイズの目安 |
| --- | --- |
| 外部I/Oなし、ブラウザ内の静的画面だけ | Small候補 |
| localhostのFrontend／API、ローカルファイルのダウンロード | Medium候補 |
| デプロイ済みAPI、外部サービス、実環境相当の複数サービス | Large候補 |

複数の条件に該当する場合は、すべての依存を許可する最小サイズを選ぶ。`E2E = Large`とは決めつけない。サイズをファイル名へ記録し、1ファイルへ異なるサイズを混在させない。

## ケース設計

正常系だけでなく、仕様に必要な次の状態を検討する。

- 初期表示、代表入力、最小・最大・空入力、ロケール
- loading、成功、空、バリデーションエラー、APIエラー、retry、timeout
- 連打、再送、キャンセル、古い応答、ルート遷移、キーボード操作
- ダウンロード、ファイル名、レスポンシブ表示、404、ErrorBoundary復旧

各ケースは入力条件、ユーザー操作、利用者が確認できる結果、根拠、優先度を持つ。同じ画面でも検証する振る舞いが異なる場合は分け、実装詳細やDOM構造をテスト名・Thenへ書かない。

## アサートなしの足場

PlaywrightにはVitestの`test.todo`がないため、未実装ケースは`test.skip`で表す。`test.skip`の本体には計画コメントだけを置き、空の成功テストにしない。

```ts
test.skip("downloads a PNG for the standard image type", async ({ page }) => {
  // ID: IMAGE-GENERATION-E2E-S-001
  // Source: docs/v1/ui/ui.md § 6, § 8, § 10
  // Given: The real API is available and the form contains valid values
  // When: The user selects the standard image type and submits the form
  // Then: A generated PNG is downloaded automatically
  // Blocked by: E2E service lifecycle
  // Priority: P0
});
```

ルール:

- `// ID`、`// Source`、`// Given`、`// When`、`// Then`、必要な`// Error`または`// Blocked by`、`// Priority`をこの順で、対象ケースの本体内へ書く。
- IDはファイル内で一意にする。テスト名には優先度やIDを重複して埋め込まない。
- `expect`、`page.route`、MSW、API stub、fixture、ダウンロード保存処理、セレクター、入力値プロバイダーは計画段階では書かない。
- APIをモックしたケースを実API接続のE2Eとして記述しない。モックが必要な場合は別のテスト層として扱う。
- Playwrightが実行できる構文にし、未実装ケースが成功扱いにならないよう`test.skip`を使う。

## ファイル配置

既存規約がなければ、対象とサイズごとに分けて`e2e/<subject>.<size>.test.ts`を使う。Playwright設定が`.spec.ts`を要求する場合は、その規約を優先し、サイズ表記を失わない。複数画像タイプなど同じ境界のケースは同じサイズファイルに置けるが、異なるサイズのケースを混在させない。

## 実装へ移行するとき

このスキルでは実装しない。後続の実装では、まず`test.skip`を1ケースだけ実テストへ変換し、実サービス境界を確認してから、ユーザー向けの入力・出力・副作用をassertする。既存の下位層テストで証明済みの内部処理を再アサートせず、E2E固有のルート接続、ブラウザ挙動、サービス統合だけを残す。

## 出力契約

次の順序で報告する。

1. ケース一覧（ID、層、サイズ、入力、操作、期待結果、根拠、優先度）
2. 作成したサイズ別ファイルと`test.skip`一覧
3. 各ケースの依存境界とサイズ選択理由
4. assertion／fixture／mockを追加していないこと
5. 検証コマンド、Skipped件数、未実行項目
6. 未解決のサービス環境、認証、外部API、データ、並行実行リスク
