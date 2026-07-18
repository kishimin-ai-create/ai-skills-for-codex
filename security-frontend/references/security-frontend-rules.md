# Security: Web Frontend Rules

## Security Headers (V3.4)

- すべてのレスポンスへ`Strict-Transport-Security`を設定し、`max-age`を1年以上にする。L2以上では`includeSubDomains`を含める。
- すべてのレスポンスへ`Content-Security-Policy`を設定する。最低限`object-src 'none'`と`base-uri 'none'`を含め、許可リスト、nonce、またはハッシュを使用する。L3ではレスポンスごとのnonceまたはハッシュを使用する。
- `Access-Control-Allow-Origin`は固定の許可リスト値とし、機密データを含むレスポンスで`*`を使わない。
- MIMEスニッフィングを防ぐため、すべてのHTTPレスポンスへ`X-Content-Type-Options: nosniff`を設定する。
- 機密URLパスが第三者へ漏れないよう`Referrer-Policy`を設定する。
- iframe埋め込みは`X-Frame-Options`ではなくCSPの`frame-ancestors`で制御する。
- tabnabbingを防ぐため、ドキュメントレスポンスへ`Cross-Origin-Opener-Policy: same-origin`または`same-origin-allow-popups`を設定する。

## Cookies (V3.3)

- すべてのCookieへ`Secure`属性を設定する。
- サブドメイン間で共有しないCookieには`__Host-`、共有する場合は`__Secure-`プレフィックスを使用する。
- Cookieの用途に適した`SameSite`属性を設定し、CSRF防御へ反映する。
- クライアントスクリプトが不要なセッショントークンなどには`HttpOnly`を設定する。
- Cookieの名前と値の合計を4096バイト未満に保つ。

## CSRF and Origin Separation (V3.5)

- CORS preflightで保護されない機密操作では、CSRFトークンを検証するか、単純リクエストに含まれないカスタムヘッダーを要求する。
- CORS preflightへ依存する場合、preflightを発生させずに到達できないことを確認する。
- 状態変更にはPOST、PUT、PATCH、DELETEを使い、GET、HEAD、OPTIONSを使わない。例外時は`Sec-Fetch-*`ヘッダーを検証する。
- `postMessage`の受信側で`Origin`を検証し、信頼できないオリジンのメッセージを破棄する。
- クロスサイトスクリプトインクルージョン（XSSI）を防ぐためJSONPを完全に無効化する。
- 認可が必要なデータをスクリプトレスポンス（JSファイル）へ含めない。

## Content Rendering (V3.2)

- テキスト表示には`createTextNode`や`textContent`など安全なDOM APIを使い、意図しないHTML・JavaScript実行を防ぐ。
- 不正なコンテキストでの表示を防ぐため、`Sec-Fetch-*`、`Content-Disposition: attachment`、またはCSP `sandbox`を適用する。
- 明示的な変数宣言、厳格な型チェック、名前空間分離でDOM clobberingを防ぐ。

## External Resources (V3.6)

- 外部ホストのJavaScript、CSS、WebフォントにはSubresource Integrity（SRI）を使用する。

## Other Browser Security (V3.7)

- Flash、ActiveX、Silverlight、NPAPI、Javaアプレットなどの廃止技術を使わない。
- 自動リダイレクト先は許可リストのホスト名だけにし、外部ドメインへ遷移する前に警告を表示する。
- ブラウザレベルの強制を最大化するため、トップレベルドメインをHSTS preloadリストへ追加する。

## Review Evidence

- 実際のレスポンスヘッダー、Cookie属性、CSP違反、CORS拒否を確認する。
- 状態変更、`postMessage`、埋め込み、リダイレクト、DOM描画の拒否テストを確認する。
- 外部リソースのSRIと許可リスト、廃止技術の不使用を確認する。
