# Security: Authorization and Tokens Rules

OWASP ASVS 5.0の認可・アクセス制御・Self-contained Token領域（V8、V9）を対象とする。

## Authorization design (V8.2)

- Function-level access controlを強制し、許可されたEndpointだけを呼び出せるようにする。
- Data-level access control（IDOR/BOLA）を強制し、RouteだけでなくすべてのData Objectの所有権・権限を検証する。
- Field-level access control（BOPLA）を強制し、権限に応じて読み書き可能なFieldを制限する。
- JavaScript変数、Hidden FieldなどClient側の状態を認可判断に使用しない。Backendで強制する。

## Access control rules

- Least Privilegeを適用し、必要最小限の権限だけを与える。
- 認可チェックを直ちに実行し、Cacheや後段処理へ遅延させない。
- Multi-tenantシステムではTenant越境を防ぎ、一つのTenantの操作が別TenantのDataへ影響しないようにする。
- 管理者画面ではNetwork Locationだけに依存せず、継続的なIdentity検証、Device Posture、Contextual Risk Analysisを要求する。

## Adaptive authorization (V8.2.4)

- 時刻、場所、IP、DeviceなどのContext属性をAuthentication・Authorization判断へ利用する。
- 新しいSession開始時だけでなく、継続中のSessionでもAdaptive Checkを適用する。

## Self-contained Token / JWT (V9)

### Token integrity (V9.1)

- Token内のClaimを信頼する前にDigital SignatureまたはMACを検証する。
- Contextごとに許可アルゴリズムのAllowlistを使用し、`none`アルゴリズムを決して受け入れない。
- Key Sourceを事前設定した信頼済みAllowlistと照合し、信頼できない`jku`、`x5u`、`jwk` Headerを拒否する。

### Token content (V9.2)

- `nbf`と`exp` Claimを検証し、有効期間外のTokenを拒否する。
- Token Typeが用途と一致することを検証する（認可にはAccess Tokenだけ、IdentityにはID Tokenだけを受け入れるなど）。
- `aud`（Audience）ClaimをServiceごとのAllowlistと照合し、別ServiceでのToken再利用を防ぐ。
- 同じPrivate Keyが複数AudienceのTokenへ署名する場合、各TokenにAudience制限を要求する。

## Common JWT pitfalls

- `alg: none`を信頼しない。
- Token Headerを未検証のままSigning Keyの動的決定に使用しない。
- Access TokenをID TokenやSession Cookieとして相互利用しない。
- XSSリスク低減のため、JWTを`localStorage`へ保存せず、`httpOnly` Cookieなどを使用する。

## Review evidence

- Endpoint、Object、Field、Tenantごとの認可を検証したか。
- Client状態に依存せず、Backendで所有権と権限を確認しているか。
- Least Privilege、即時チェック、管理者の継続Identity・Device・Risk確認を適用したか。
- JWTの署名、アルゴリズム、Key Source、`nbf`、`exp`、`aud`、用途を検証したか。
- Tenant越境、権限昇格、Token再利用、Context変化、失効をテストしたか。
