---
name: explain-aspnet-core-code
description: 指定されたASP.NET CoreのC#コードを、構文、責務、DI、Middleware、Routing、ControllerまたはMinimal API、Model Binding、Validation、Configuration、認証・認可、例外処理、レスポンス、バックエンド層の関係に分解して日本語で説明する。Program.cs、Controller、Middleware、Filter、Service登録、Options、HTTP APIなどの処理内容やリクエストフローを理解したいときに使用する。
---

# Explain ASP.NET Core Code

指定されたASP.NET Coreコードを、対象リポジトリから確認できる事実に基づいて日本語で説明する。

## 調査手順

1. 指定されたファイルまたはコード範囲を全文読む。
2. 対象プロジェクトの`.csproj`を読み、Target Framework、SDK、Nullable、主要Packageを確認する。
3. `Program.cs`またはStartup相当のコードを確認し、Hosting方式、Service登録、Middleware順序、Endpoint登録を特定する。
4. 説明に必要な直接の依存先だけを追う。Interface、実装、DTO、Options、Model、拡張メソッドの順に参照関係を確認する。
5. 関連する仕様、ADR、設定ファイルがある場合は、対象コードへ直接影響する箇所だけを読む。
6. HTTP入口からレスポンスまでを追える場合は、実行順に並べ直す。

説明だけを求められた場合は、ファイルを変更せず、アプリケーション、テスト、ビルドを実行しない。診断、レビュー、修正、実行結果も求められた場合だけ追加作業を行う。

## 説明する内容

### ファイルの役割

- アプリケーション起動、HTTP境界、Application Service、Domain、Infrastructureのどこに属するか
- クラス、record、Interface、メソッド、属性、拡張メソッドの役割
- ASP.NET Core固有部分と通常のC#部分の区別
- 入力、戻り値、副作用、外部依存

### リクエストフロー

該当する段階だけを実際の順序で説明する。

```text
HTTP Request
  -> Middleware Pipeline
  -> Routing
  -> Authentication / Authorization
  -> Model Binding / Validation
  -> Endpoint / Controller
  -> Service / Domain / Infrastructure
  -> Result conversion
  -> HTTP Response
```

`Use*`の記述順と実行順を確認する。コードに存在しないMiddlewareや処理を補完しない。Endpoint Routing、Exception Handler、CORS、Rate Limiting、Static Filesなどは、登録されている場合だけ説明する。

### Dependency Injection

- `AddSingleton`、`AddScoped`、`AddTransient`のうち使用されているLifetime
- 登録されるService型と実装型
- Constructor InjectionまたはParameter Injectionによる解決箇所
- `AddHttpClient`、Options、Factoryなどの生成境界

Lifetimeの一般論を長く書かず、対象コードでインスタンスが共有される範囲と、その依存関係を説明する。

### HTTP境界

- Route、HTTP Method、Header、Query、Route Value、Bodyの取得元
- DTOからApplicationまたはDomain型への変換
- Model Binding、Validation、Filter、Attributeの働き
- `IActionResult`、`ActionResult<T>`、`IResult`、Typed Resultsなど、実際の戻り値から生成されるResponse
- Status Code、Content-Type、Header、Body
- CancellationToken、非同期処理、例外変換

コードだけでは最終Status Codeなどを断定できない場合は、その条件を明示する。

### Configurationと実行環境

- `appsettings*.json`、環境変数、User Secrets、Options Bindingのうち、コードで確認できる入力元
- Development、Productionなど環境分岐
- 値の取得、検証、利用箇所

秘密値の実値は出力しない。設定の優先順位は、対象コードと構成から確認できる範囲だけ説明する。

### バックエンド層

依存方向を次の観点で整理する。

```text
HTTP boundary -> Application Service -> Domain
                       |
                       v
                    Port <- Infrastructure Adapter
```

ControllerまたはEndpointはRequest解析とResponse変換、ServiceはUse Case、Domainは業務ルール、InfrastructureはHTTP・DB・Framework詳細として説明する。リポジトリ独自の構成がある場合は、そちらを優先する。

## 出力形式

対象の規模に合わせ、必要な見出しだけを使用する。

```markdown
## 概要

## コードの構成

## 処理の流れ

## ASP.NET Coreの仕組み

## DIと依存関係

## 入出力

## 関連コード
```

短いコードでは行またはブロック単位で説明する。複数ファイルにまたがる場合は、最初に全体フローを示してから各ファイルの責務を説明する。

## 正確性

- コード、Frameworkの既定動作、設定、仕様、推測を区別する。
- 推測には「推測」と明記し、根拠となるコードが不足していることを示す。
- Service登録と実際の利用を混同しない。
- Middlewareの登録順を無視して一般的な順序を断定しない。
- Interfaceの契約と実装詳細を分ける。
- 非同期メソッドを並列実行と説明しない。
- 認証と認可、Model BindingとValidationを区別する。
- レビューや改善案は、ユーザーが求めた場合だけ提示する。
- 行番号を示す場合は、読み取った実ファイルの行番号を使用する。
