# Security: API and Communication Rules

OWASP ASVS 5.0のAPI・通信領域（V4、V12）を対象とする。

## HTTP API hygiene (V4.1)

- 本文のあるすべてのHTTP応答で、charset付きの`Content-Type`を設定する。
- HTTPからHTTPSへのリダイレクトは利用者向けブラウザエンドポイントだけで行う。その他のサービスは暗黙にリダイレクトしない。
- Proxyが設定した`X-Real-IP`、`X-Forwarded-*`、`X-User-ID`などの中間ヘッダーをエンドユーザーが上書きできないようにする。
- APIが明示的にサポートするメソッドだけを許可し、不要なHTTPメソッドを拒否する。

## HTTP request smuggling (V4.2)

- HTTPバージョンごとにメッセージ境界を判定する。HTTP/1.xでは`Transfer-Encoding`を`Content-Length`より優先し、HTTP/2・HTTP/3では`Content-Length`とDATAフレーム長が一致することを検証する。
- HTTP/2・HTTP/3で接続固有ヘッダー（`Transfer-Encoding`など）を含むメッセージを拒否する。
- HTTP/2・HTTP/3のヘッダーにCR、LF、CRLFのシーケンスが含まれる場合は拒否する。
- URIとヘッダーフィールドの長さを制限し、過長リクエストによるDoSを防ぐ。

## GraphQL (V4.3)

- ネストしたクエリによるDoSを防ぐため、クエリ深度制限、量（amount）制限、またはクエリコスト分析を実装する。
- 本番のGraphQLイントロスペクションは、APIを公開する設計上の理由がない限り無効化する。

## WebSocket (V4.4)

- すべてのWebSocket接続にWSS（TLS上のWebSocket）を使用する。
- 初回WebSocketハンドシェイクの`Origin`を許可リストと照合する。
- WebSocket専用の準拠したセッションTokenを使用し、Upgrade時に確立済みHTTPSセッションと照合する。

## TLS configuration (V12)

- TLS 1.2とTLS 1.3だけを有効にし、TLS 1.3を優先する。
- 承認済みの暗号スイートだけを有効にする。ASVS L3では前方秘匿性を持つ暗号スイートだけを使用する。
- 外部公開サービスでは、公的に信頼されたTLS証明書を使用する。
- mTLSでは、認証・認可判断に利用する前にクライアント証明書を検証する。
- TLSクライアントは通信前にサーバー証明書を検証する。
- 内部サービス間のHTTP通信もTLSを使用し、平文へフォールバックしない。
- 内部TLS接続では、信頼された証明書（内部管理CAまたは明示的に管理された自己署名証明書）を使用する。
- マイクロサービスでは、相互TLS証明書管理を簡素化するためService Meshを検討する。
- ASVS L3では、証明書失効確認のためOCSP Staplingを有効にする。

## Review evidence

- 対象プロトコルとHTTPバージョンを記録する。
- 許可メソッド、最大URI・ヘッダー長、GraphQL制限、WebSocket Origin許可リストを確認する。
- TLSバージョン、暗号スイート、証明書チェーン、失効確認、mTLS設定を確認する。
- 失敗時に安全側へ倒れること、内部詳細やProxy信頼情報が上書き・漏えいしないことを検証する。
