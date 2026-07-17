---
name: frontend-security
description: "Webフロントエンドにおける認証、認可、トークン管理、安全なローカル開発ネットワークパターン。"
---

# Frontend Security

認証・認可パターンを選定する場合や、フロントエンド側のセキュリティ境界を扱う場合に、このスキルを使用する。

## Security Baseline

- フロントエンドコードはユーザーが制御できるため、信頼できるセキュリティ境界として扱わない。
- フロントエンドのセキュリティ制御は、UXの改善や操作ミスの削減には利用できるが、本質的な保護はバックエンドで実施する。
- 独自認証を構築するより、外部のIdentity Providerを優先する。

## Authentication Patterns

| Pattern                                          | Best for                                         | Strengths                                                                          | Risks / trade-offs                                                                                     |
| ------------------------------------------------ | ------------------------------------------------ | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Frontend-only OIDC**                           | IdPのJWTを直接利用できる単純なアーキテクチャ     | 柔軟性が高く、サーバー側のCallback状態が不要                                       | フロントエンドでAuthorization Code + PKCEが必要、Logoutが複雑、アプリ固有のClaimが不足する可能性がある |
| **OIDC -> server callback -> session cookie**    | セキュリティを優先するWebアプリ                  | フロントエンドへのToken露出が少ない、Logoutが容易、サーバーSession保存と相性が良い | フロントエンドはアプリ情報をバックエンドから取得する必要があり、サーバー側の認証処理が増える           |
| **OIDC -> server callback -> server-issued JWT** | アプリ固有のClaimをTokenへ含める必要があるアプリ | アプリ固有のClaimを埋め込みやすく、フロントエンドで認可情報を扱いやすい            | 証明書・鍵の管理、Token検証の負担、Token保存方法の判断が必要                                           |
| **Home-grown ID/password**                       | ごく限られた例外                                 | 最大限の制御が可能                                                                 | コストとリスクが高く、通常は割に合わない                                                               |

## Default Recommendations

- Enterprise IdP、Cognito、Auth0、Firebaseなどの**外部OIDC Provider**を優先する。
- 多くのWebアプリでは、**server callback + session cookie**を最も安全なデフォルトとする。
- フロントエンドがアプリ固有のClaimを可搬性のあるTokenとして本当に必要とする場合は、**server-issued JWT**を使用する。
- 要件上ほかに現実的な選択肢がない場合を除き、独自のユーザー名・パスワード認証は構築しない。

## Token and Session Handling

### Frontend-only OIDC

- APIリクエスト時にTokenを送信する。
- 本当に必要なClaimだけを解析する。
- Logout時はIdPのLogout Endpointへリダイレクトする。
- バックエンドではIssuer、有効期限、署名を含むJWT検証を必ず行う。

### Session Cookie Model

- IdPのTokenはサーバー側に保持する。
- フロントエンドは必要なユーザー情報をバックエンドから取得する。
- Session Cookieが存在しない、または無効な場合は、Login Flowを開始する契機として扱う。

### Server-Issued JWT Model

- Server Callbackを利用し、フロントエンドが必要とするClaimを追加する。
- Server-issued JWTは、すべてのリクエストで検証する。
- 署名鍵と証明書のRotationを慎重に管理する。

## Authorization Rules

フロントエンドの認可は**UXのため**に存在し、本質的な防御にはならない。

### What frontend authorization should control

- RouteやScreenへのアクセス
- Screen内のUI要素の表示・非表示

### What frontend authorization must not replace

- バックエンドAPIの認可
- データアクセス制御
- ユーザー本人確認と権限に関するサーバー側検証

## Authorization Design Guidance

- 過度なコンポーネント単位の権限ロジックより、**ページ単位のアクセス制御**を優先する。
- Route保護にはRouter GuardやNavigation Guardを使用する。
- コンポーネント単位の表示可否チェックは最小限にする。
- TokenにRole Identifierが含まれる場合は、フロントエンド側のPermission Mapを単純かつ効果的に構成できる。
- RoleやPermissionを業務ユーザーが動的に管理する場合は、ハードコードせずバックエンドから取得する。

## Storage Guidance

- Session IDをURLに含めない。
- 機密性の高い値をQuery Parameterで公開しない。
- SessionベースのLoginにはCookieを優先する。
- Offline UXのために認証関連のユーザー情報を保存する場合は、必要最小限に留め、再接続時にはバックエンドが実際のユーザーを引き続き検証するようにする。

## Logout Guidance

- Federated Loginでは、ローカルでLogoutするだけでは不十分である。
- IdP Sessionが存在する場合は、IdP側のLogout Flowも完了させる。
- Tokenの有効期間とLogout挙動を、実際のセキュリティモデルと一致させる。

## Local Development and CORS

開発環境でフロントエンドとAPIが別のSubdomainやPortを使用する場合でも、不要なCORS回避策を本番コードへ持ち込まない。

### Options

| Approach                                  | Recommendation                                         |
| ----------------------------------------- | ------------------------------------------------------ |
| APIアプリへ直接CORS処理を追加する         | 許容可能だが、本番では不要なコードが増える可能性がある |
| nginxなどのReverse Proxyを使用する        | チームがすでに利用している場合は適切                   |
| フロントエンドDev ServerのProxyを使用する | 推奨するデフォルト                                     |

### Recommended Vite Pattern

```ts
import { defineConfig } from "vite";

export default defineConfig({
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8080",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
```

## Security Reminders

- データ整合性とXSS対策のため、標準的な入力バリデーションは引き続きサーバー側で実施する。
- 必要なSecurity Headerを付与できるHostingを選ぶ。
- 特に多くのクライアントライブラリを利用するCSR中心のアプリでは、Third-party Dependencyのリスクに注意する。
- UIを非表示にしただけで、データが保護されているとは考えない。
