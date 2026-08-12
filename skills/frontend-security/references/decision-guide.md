# Frontend Security Decision Guide

## 認証・セッション

- Identity Providerと標準プロトコルを優先し、独自のパスワード保管・認証フローを増やさない。
- ブラウザで扱うトークンは、HttpOnly Cookie、短命アクセストークン、BFFなどを脅威モデルで比較する。
- localStorageはXSS時の窃取リスクを明示し、採用する場合は有効期限、失効、CSP、影響範囲を定義する。
- CookieはHttpOnly、Secure、SameSite、Domain、Path、期限、CSRF対策を一組で決める。

## 脅威と対策

| 脅威 | 基本対策 |
| --- | --- |
| XSS | 出力エスケープ、危険HTML禁止、CSP、依存関係管理 |
| CSRF | SameSite、CSRFトークン、Origin/Referer検証 |
| IDOR・権限昇格 | サーバー側の対象リソース・権限再検証 |
| Open Redirect | 相対パスまたはallowlist、正規化 |
| クリックジャッキング | frame-ancestors、X-Frame-Options |
| 情報漏えい | エラー・ログ・URL・分析イベントの秘匿 |
| 依存関係侵害 | lockfile、最小依存、スキャン、更新レビュー |

## Security Header

- CSP、HSTS、X-Content-Type-Options、Referrer-Policy、Permissions-Policyを環境ごとに確認する。
- 機能や外部サービスの許可範囲を先に列挙し、unsafeな緩和を既定値にしない。

## 開発プロキシ

- 転送先、パス、Origin、Host、認証ヘッダー、タイムアウトをallowlistで制限する。
- 本番の認証・CORS・TLS・Headerポリシーを開発プロキシの成功だけで判断しない。

## 採用を見送る条件

- クライアント側の非表示だけでデータを保護する。
- ワイルドカードCORS、無期限トークン、検証なしreturn URL、危険HTML挿入を採用する。
- 脆弱性スキャンの結果を確認せず依存関係を追加する。
