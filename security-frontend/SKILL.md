---
name: security-frontend
description: Webフロントエンドのセキュリティヘッダー、Cookie、CSP、CSRF、CORS、ブラウザ保護、DOM描画、外部リソースを設計・実装・レビューするときに使用する。OWASP ASVS 5.0 V3を扱う。
---

# Security: Web Frontend

ブラウザ境界を変更するときは、実行コンテキスト、信頼するオリジン、認証Cookie、外部リソース、表示データを確認し、詳細規則を [references/security-frontend-rules.md](references/security-frontend-rules.md) から該当範囲だけ読む。

## Workflow

1. ドキュメント、API、iframe、Worker、外部リソースのオリジンとデータフローを特定する。
2. レスポンスヘッダー、Cookie属性、CSP/CORS、CSRF防御、DOM描画、リダイレクトを確認する。
3. V3の該当規則を適用し、必要なブラウザ互換性と環境差を明示する。
4. 最小変更で実装し、信頼できない入力がHTML・スクリプト・遷移先として解釈されないようにする。
5. ヘッダー、Cookie、許可・拒否オリジン、状態変更、埋め込み、外部リソースのテストを実行する。
6. 適用規則、検証結果、未対応ブラウザ、残存リスクを報告する。

## Non-negotiable rules

- HSTS、CSP、`nosniff`、Referrer-Policyなどの必要な保護ヘッダーを設定する。
- 認証Cookieには用途に応じて`Secure`、`HttpOnly`、`SameSite`と安全なプレフィックスを設定する。
- 状態変更をGETで行わず、CSRFまたはOrigin分離をサーバー側で検証する。
- DOMへ表示する文字列は安全なAPIで扱い、信頼できないHTML・スクリプトを実行させない。
- 外部JavaScript、CSS、フォントにはSRIを使用し、外部遷移先とCORSオリジンを許可リストで制限する。

## References

- [Security frontend rules](references/security-frontend-rules.md)
- API通信のTLS・HTTP規則は [security-api](../security-api/SKILL.md)、認証・認可は [security-authn](../security-authn/SKILL.md) と [security-authz](../security-authz/SKILL.md) を併用する。
