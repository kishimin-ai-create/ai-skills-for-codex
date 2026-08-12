# Backend Architecture Reference

## Directory structure

```text
src/
├── models/                # Domain Model: Entities / Value Objects
├── services/              # Application Service: Usecase / Business Logic
├── repositories/          # Repository Interfaces and access boundary
├── controllers/           # HTTP entry point
└── infrastructures/       # DB, APIs, frameworks, external systems
```

## Layer responsibilities

| Layer          | Responsibility                                                   | Must not do                             |
| -------------- | ---------------------------------------------------------------- | --------------------------------------- |
| Model          | Entities、Value Objects、business rules                          | 他レイヤー、framework、DB、HTTPへの依存 |
| Service        | Business logic、Usecase orchestration                            | SQL、HTTP、Infrastructure詳細           |
| Repository     | Persistence boundary; InterfaceはModel側、実装はInfrastructure側 | Infrastructure errorの漏出              |
| Controller     | Request/response mapping、Service呼び出し                        | 業務ロジック、直接DBアクセス            |
| Infrastructure | DB、外部API、framework、adapter                                  | 業務ロジックを内包すること              |

## Dependency direction

```text
Controller → Service → Model
           ↓
      Repository (interface)
           ↓
    Infrastructure (implementation)
```

依存は内側へ向ける。Modelは外側を知らず、ControllerやInfrastructureからModelへ向かう依存をInterface・Portで表現する。

## Error boundary

- Infrastructureで発生したDB、HTTP、SDKなどのエラーを、そのままControllerやModelへ返さない。
- Repositoryまたはadapter境界で、利用側が判断できるDomain固有のエラー（例: `AppError`、`RepoError`）へ変換する。
- ControllerはDomain/Application errorをHTTP statusと安全な公開メッセージへ変換する。
- stack trace、SQL、認証情報、内部URLなどの内部詳細を公開レスポンスへ含めない。

## Review questions

- 新しいimportは依存方向を逆転させていないか。
- ServiceへSQLやHTTPを追加していないか。
- Controllerへ業務ルールを追加していないか。
- Repository InterfaceがInfrastructure型を公開していないか。
- Infrastructureの失敗がDomain/Application errorへ変換されているか。
- 既存のADRや外部契約と矛盾していないか。
