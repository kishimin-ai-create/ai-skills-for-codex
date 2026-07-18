---
name: security-api
description: APIとWebサービスのHTTP、GraphQL、WebSocket、TLS/通信セキュリティをOWASP ASVSの観点で設計・実装・レビューするときに使用する。
---

# Security: API and Communication

API通信を変更する前に、公開範囲、プロトコル、信頼境界、許可メソッド、認証情報、TLS終端を確認する。

## Workflow

1. API、GraphQL、WebSocket、内部サービス通信の対象と攻撃面を特定する。
2. [references/security-api-rules.md](references/security-api-rules.md)から該当する規則を読む。
3. HTTPヘッダー、メソッド、メッセージ境界、入力長、リダイレクト、Origin、TLS証明書を検証する。
4. 本番・内部通信・開発環境で異なる設定を分離し、安全側の失敗を確認する。
5. 設定、統合テスト、負荷・異常系テスト、TLS検証を実行する。
6. 適用したASVS領域、検証結果、残存リスク、未対応項目を報告する。

## Non-negotiable rules

- サポートしないHTTPメソッド、プロトコル、ヘッダー、過長入力を拒否する。
- HTTP/2・HTTP/3で接続固有ヘッダーや改行を許可しない。
- GraphQLの深さ・量・コストを制限し、本番イントロスペクションを必要性なく公開しない。
- WebSocketはWSSを使用し、Originと専用セッションTokenを検証する。
- TLS 1.2/1.3のみを使用し、証明書とサーバー／クライアントの検証を省略しない。
- 内部サービス間通信でも平文へフォールバックしない。

## References

- [Security API rules](references/security-api-rules.md)
