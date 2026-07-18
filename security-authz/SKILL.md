---
name: security-authz
description: 機能・データ・フィールド単位の認可、マルチテナント分離、適応型アクセス制御、JWTとSelf-contained TokenをOWASP ASVSの観点で設計・実装・レビューするときに使用する。
---

# Security: Authorization and Tokens

認可やTokenを変更する前に、主体、対象Resource、操作、Tenant、Context、Token発行者と受信者を明確にする。

## Workflow

1. Endpoint、Resource、Field、Tenant、管理者操作の権限モデルを特定する。
2. [references/security-authz-rules.md](references/security-authz-rules.md)から該当規則を読む。
3. Backendで機能・データ・フィールド単位の認可を評価し、Client状態を信頼しない。
4. JWTの署名、アルゴリズム、Key Source、Claims、Audience、有効期間、保存方式を検証する。
5. Tenant越境、権限昇格、Token再利用、失効、Context変化をテストする。
6. 認可決定、監査証跡、検証結果、残存リスクを報告する。

## Non-negotiable rules

- 認可はBackendで実行し、Clientの変数、Hidden Field、表示状態を根拠にしない。
- Endpoint、各Data Object、各Fieldの権限を検証する。
- Least PrivilegeとTenant Isolationを適用する。
- JWTの署名・MAC、許可アルゴリズム、Key Source、`nbf`、`exp`、`aud`を検証する。
- `alg: none`、未検証の`jku`・`x5u`・`jwk`、用途外Tokenを拒否する。
- JWTを`localStorage`へ保存せず、Webでは`httpOnly` Cookieなど、対象環境の安全な保存方式を使う。

## References

- [Security authorization rules](references/security-authz-rules.md)
