---
name: xunit-aspnet-core-test-case-design
description: Design behavior-focused, comment-only xUnit test plans for ASP.NET Core applications without writing test code. Use when deriving test TODO comments from requirements, API contracts, domain models, controllers, middleware, authentication, persistence, external HTTP integrations, or existing .NET tests; choose the smallest reliable test level and report unimplemented cases, execution evidence, and residual risks.
---

# xUnit ASP.NET Core Test Case Design

テスト対象の実装詳細ではなく、利用者から観測できる振る舞い・事後条件・不変条件を、コメントだけの xUnit 実装計画へ落とし込む。テストコードは書かない。

## Comment-only constraint

- 新規・既存を問わず、テストファイルへ追加できるのは `//` で始まるコメントだけとする。
- `[Fact]`、`[Theory]`、テストメソッド、クラス、fixture、fake、stub、assertion、`using`、プロジェクト設定を生成・変更しない。
- コメントにはテスト名、前提条件、操作、期待結果、必要な境界・fixture、根拠、優先度を記録する。
- コメントを skipped test や実装済みテストとして扱わず、常に未実装として報告する。
- 既存テストコードは設計根拠の確認と実行に限って読み取り、書き換えない。

## Workflow

1. 対象プロジェクトを特定する。`*.sln`、`*.csproj`、`global.json`、既存の `*.Tests.cs`、`*.test.cs`、`Program.cs`、API仕様、ADRを確認する。
2. テストランナーと実行コマンドを検出する。標準コマンドは `dotnet test` とし、既存の solution、test project、filter、coverage 設定を優先する。
3. 境界を列挙する。Domain、Application、Controller、Middleware、認証認可、DB、外部HTTP、時刻、乱数、ファイル、キュー、レート制限を分離する。
4. 状態表を作る。各ケースに ID、層、入力、操作、期待する出力・状態・副作用、根拠、優先度を記録する。
5. 正常、代替、境界、異常、空値、型不正、ロケール、再実行、連打、並行要求、キャンセル、タイムアウト、認証・認可をリスクに応じて網羅する。
6. 最小のテスト層を選ぶ。内部ロジックは Unit、HTTP契約は ASP.NET Core Integration、外部サービス契約は HTTP 境界の Contract、主要利用者フローだけを E2E とする。
7. 未実装ケースを「未実装テスト一覧」として出力し、対象テストファイルへ書き込む場合はコメントだけで記録する。属性や空のテストメソッドをプレースホルダーとして作らない。
8. 既存の実装済みテストが公開契約を検証しているか読み取る。内部メソッド、private state、具体的なDI登録順、脆いJSON順序、HTML構造を根拠なく計画へ固定しない。
9. `dotnet test` を対象プロジェクトから実行し、成功・失敗・Skipped・未実行を分けて報告する。失敗は実装・テスト・環境・仕様のいずれかに分類し、推測を原因として断定しない。

## Test-level selection

| 層 | xUnit / ASP.NET Core の境界 | 主な対象 |
| --- | --- | --- |
| Unit | 通常の xUnit test class、fake、stub | Value Object、Domain invariant、変換、純粋なサービス、状態遷移 |
| Integration | `WebApplicationFactory<TEntryPoint>`、`TestServer`、`HttpClient` | Routing、model binding、validation、middleware、認証、ProblemDetails、DB接続 |
| Contract | 実HTTP境界または契約に沿った test host / fake upstream | Status、headers、JSON schema、外部APIの成功・失敗・timeout mapping |
| E2E | 実行環境に対する少数の利用者フロー | 認証から主要操作・重要エラーまでの横断フロー |

Unit で証明できる分岐を Integration や E2E に重複させない。ただし HTTP status、serialization、DI、middleware、認証境界は Unit の mock だけで代替しない。

## Case design rules

- テスト名は「条件・操作・期待結果」を表す。例: `PostImages_WhenTextExceedsLimit_ReturnsUnprocessableEntity`。
- データ駆動が適するケースはコメント内で Theory 候補と記録し、異なる理由の失敗を一つの曖昧なケースへまとめない。属性やテストコードは書かない。
- 文字列では空、null、空白のみ、最小、最大、最大超過、Unicode grapheme、制御文字を区別する。
- APIではHTTP method、route、status、content type、body、error code、field、localized message、外部呼び出しの有無を必要な範囲で検証する。
- Authentication と Authorization を分ける。未認証、認証済み・権限不足、権限ありを別ケースにする。
- 外部HTTPのfakeはレスポンス、遅延、切断、timeout、Retry-After、malformed payloadを制御できる境界に置く。fakeの呼び出し回数や送信内容は副作用契約として必要な場合だけ検証する。
- DBを使うテストはデータ分離と後片付けを明示する。共有fixtureを使う場合は並行実行の安全性を証明する。
- 時刻・乱数・UUIDを固定する必要がある場合は注入境界を使い、グローバル時計や実時間待機に依存しない。
- リトライを検証する場合は、重複副作用、キャンセル、timeout、idempotency の条件を必ず確認する。

## ASP.NET Core integration rules

- `WebApplicationFactory<Program>` を使う場合、テストが必要とする差し替えは専用の factory / `ConfigureTestServices` に閉じ込める。
- `HttpClient` を実際のアプリケーション境界として使い、request、response、headers、status、serializationを観測する。
- 外部APIを差し替える場合、アプリケーションの `HttpClient` が実際に通る handler または test server を差し替える。service自体をmockしてControllerだけを通す方法は、HTTP・DTO・例外変換の契約を証明しない。
- `ProblemDetails` や独自エラー形式は、status と本文の主要フィールドを検証する。未要求の全文文字列やJSONプロパティ順序は固定しない。
- test host の環境変数、認証スキーム、DB、外部HTTP、ポートはテスト間で共有しない。共有が避けられない場合はfixtureの所有権と並行実行制約を明記する。
- レート制限、timeout、cancellation は実時間の長い待機を避け、制御可能な clock / handler / options を使って境界を検証する。

詳細な xUnit パターンは [references/xunit-patterns.md](references/xunit-patterns.md)、ASP.NET Core の層と境界は [references/aspnet-core-levels.md](references/aspnet-core-levels.md) を必要なときに読む。

## Output contract

次の順序で簡潔に出力する。

1. **Test list**: ID、テスト層、シナリオ、入力、期待結果、根拠、優先度。
2. **Unimplemented tests**: コメントとして記録した xUnit のテスト名、実装条件、優先度。すべて未実装として扱う。
3. **Layer selection**: なぜその層が最小で十分か、なぜ他層へ重複させないか。
4. **Execution**: 既存テストの実行コマンド、対象プロジェクト、結果、失敗分類、Skipped、未実行。コメントで追加したケースは未実行として扱う。
5. **Requirement mapping**: 要件・API契約・ADRとテストケースの対応。
6. **Residual risks**: 未検証条件、環境依存、並行性、外部サービス、仕様確認事項。
