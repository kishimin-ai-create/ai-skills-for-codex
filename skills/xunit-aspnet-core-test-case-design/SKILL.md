---
name: xunit-aspnet-core-test-case-design
description: Design and scaffold behavior-focused xUnit placeholder tests for ASP.NET Core applications, classified into Small, Medium, and Large files. Use when deriving tests from requirements, API contracts, domain models, controllers, middleware, authentication, persistence, external HTTP integrations, or existing .NET tests; create per-subject, per-size test files with matching class names, skipped test functions, and complete planning comments without assertions or production implementation.
---

# xUnit ASP.NET Core Test Case Design

テスト対象の実装詳細ではなく、利用者から観測できる振る舞い・事後条件・不変条件を、xUnit が検出できる未実装テストの足場へ落とし込む。namespace、class、テスト関数まで作成し、関数本体には実装計画コメントだけを書く。

## Scaffold contract

- 各ケースを`test-sizes`の依存境界でSmall、Medium、Largeへ分類する。速度だけで分類しない。
- 対象とサイズごとに、リポジトリ規約へ従ったテストファイルを作る。規約がなければ`SubjectSmallTests.cs`、`SubjectMediumTests.cs`、`SubjectLargeTests.cs`を使用する。複数対象を汎用的な`TestCases.cs`へまとめない。
- 配置から導かれるnamespaceと、ファイル名に一致する`public sealed class SubjectSmallTests`などのクラスを作る。
- 1ファイルへ異なるサイズを混在させない。同じ対象でも依存境界が異なる場合はサイズ別ファイルへ分割する。
- 各ケースを`public void Condition_Action_ExpectedResult()`として作り、`[Fact(Skip = "TODO: ...")]`を付ける。空の関数を成功扱いにしない。
- Theory候補は関数内コメントへ記録する。データとassertionを実装するまでは、データなしの`[Theory]`を作らずSkipped Factを使う。
- 各関数本体には`// ID`、`// Source`、`// Given`、`// When`、`// Then`、必要な`// Error`または`// Blocked by`、`// Priority`をすべて書く。
- ケース計画コメントをクラス外や関数外へ置かない。
- assertion、fixture、fake、stub、データプロバイダー、プロダクションコードは実装しない。
- 生成した関数をすべてSkippedとして報告し、実装済み・成功・coverage対象として扱わない。

## Workflow

1. 対象プロジェクトを特定する。`*.sln`、`*.csproj`、`global.json`、既存の `*.Tests.cs`、`*.test.cs`、`Program.cs`、API仕様、ADRを確認する。
2. テストランナーと実行コマンドを検出する。標準コマンドは `dotnet test` とし、既存の solution、test project、filter、coverage 設定を優先する。
3. 境界を列挙する。Domain、Application、Controller、Middleware、認証認可、DB、外部HTTP、時刻、乱数、ファイル、キュー、レート制限を分離する。
4. 状態表を作る。各ケースにID、層、サイズ、入力、操作、期待する出力・状態・副作用、根拠、優先度を記録する。
5. 正常、代替、境界、異常、空値、型不正、ロケール、再実行、連打、並行要求、キャンセル、タイムアウト、認証・認可をリスクに応じて網羅する。
6. 最小のテスト層とサイズを選ぶ。外部I/Oなしの単一プロセスはSmall、`WebApplicationFactory`、`TestServer`、制御されたDB・HTTP境界はMedium、実サービス相当または複数プロセスのE2EはLargeとする。
7. 未実装ケースごとにSkipped Fact関数を作り、詳細な計画コメントを関数本体へ書く。対象とサイズの単位でファイルを分ける。
8. 既存の実装済みテストが公開契約を検証しているか読み取る。内部メソッド、private state、具体的なDI登録順、脆いJSON順序、HTML構造を根拠なく計画へ固定しない。
9. `dotnet test` を対象プロジェクトから実行し、成功・失敗・Skipped・未実行を分けて報告する。失敗は実装・テスト・環境・仕様のいずれかに分類し、推測を原因として断定しない。

## Test-level selection

| 層 | xUnit / ASP.NET Core の境界 | 主な対象 |
| --- | --- | --- |
| Unit | 通常の xUnit test class、fake、stub | Value Object、Domain invariant、変換、純粋なサービス、状態遷移 |
| Integration | `WebApplicationFactory<TEntryPoint>`、`TestServer`、`HttpClient` | Routing、model binding、validation、middleware、認証、ProblemDetails、DB接続 |
| Contract | 実HTTP境界または契約に沿った test host / fake upstream | Status、headers、JSON schema、外部APIの成功・失敗・timeout mapping |
| E2E | 実行環境に対する少数の利用者フロー | 認証から主要操作・重要エラーまでの横断フロー |

## Test-size naming

| サイズ | 主な依存 | 既定のファイル / クラス |
| --- | --- | --- |
| Small | 単一プロセス、外部I/Oなし。Value Object、Domain invariant、純粋な変換 | `SubjectSmallTests.cs` / `SubjectSmallTests` |
| Medium | `WebApplicationFactory`、`TestServer`、制御されたDB・HTTP | `SubjectMediumTests.cs` / `SubjectMediumTests` |
| Large | 実サービス相当、実ブラウザ、複数プロセスの利用者フロー | `SubjectLargeTests.cs` / `SubjectLargeTests` |

`Unit`、`Integration`、`Contract`、`E2E`はテスト目的を説明する層であり、Small、Medium、Largeは依存範囲を示すサイズである。両者を混同しない。リポジトリに別の言語相当命名がある場合は、その規則を優先する。

Unit で証明できる分岐を Integration や E2E に重複させない。ただし HTTP status、serialization、DI、middleware、認証境界は Unit の mock だけで代替しない。

## Case design rules

- テスト名は「条件・操作・期待結果」を表す。例: `PostImages_WhenTextExceedsLimit_ReturnsUnprocessableEntity`。
- データ駆動が適するケースは関数内でTheory候補と記録し、異なる理由の失敗を一つの曖昧なケースへまとめない。実装前はSkipped Factとして可視化する。
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

1. **Test list**: ID、テスト層、サイズ、シナリオ、入力、期待結果、根拠、優先度。
2. **Unimplemented tests**: 作成したSkipped関数名、実装条件、優先度、ブロック理由。すべて未実装として扱う。
3. **Layer and size selection**: なぜその層とサイズが最小で十分か、なぜ他層へ重複させないか、作成したサイズ別ファイル。
4. **Execution**: 実行コマンド、対象プロジェクト、成功・失敗・Skippedを分けた結果。追加した足場はSkipped件数と一致させる。
5. **Requirement mapping**: 要件・API契約・ADRとテストケースの対応。
6. **Residual risks**: 未検証条件、環境依存、並行性、外部サービス、仕様確認事項。
