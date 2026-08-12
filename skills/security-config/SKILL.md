---
name: security-config
description: 秘密情報管理、サービス間通信、本番ハードニング、データ分類・保護を設計・実装・レビューするときに使用する。OWASP ASVS 5.0 V13・V14の設定セキュリティを扱う。
---

# Security: Configuration and Data Protection

設定、秘密情報、通信、データ保護を変更するときは、保護対象と信頼境界を先に特定し、詳細規則を [references/security-config-rules.md](references/security-config-rules.md) から該当範囲だけ読む。

## Workflow

1. 秘密情報、サービス間通信、公開面、保存・転送・表示されるデータを洗い出す。
2. 現在の設定、権限、環境変数、デプロイ成果物、キャッシュ、クライアント保存領域を確認する。
3. V13/V14の該当規則を適用し、環境差（開発・テスト・本番）を明示する。
4. 最小変更で実装し、秘密情報をコード・URL・ログ・応答・クライアント永続領域へ出さない。
5. 設定検証、権限境界、機密データの非露出、保持期限、失敗時の安全性をテストする。
6. 適用規則、変更、検証結果、未確認事項、残存リスクを報告する。

## Non-negotiable rules

- 秘密情報はソース、ビルド成果物、URL、ログへ置かず、承認済みのSecret管理へ保存する。
- サービス間通信は個別の認証と最小権限を使用し、外部接続先を許可リストで制限する。
- 本番ではデバッグ、TRACE、ディレクトリ一覧、意図しない内部情報・バージョン情報を公開しない。
- 機密データを分類し、必要最小限の返却、暗号化・保持・アクセス・ログ方針を適用する。
- 機密レスポンスはキャッシュさせず、セッション終了時にクライアント保存データを消去する。

## References

- [Security configuration and data protection rules](references/security-config-rules.md)
- 認証・パスワード・トークンの詳細は [security](../security/SKILL.md)、API通信は [security-api](../security-api/SKILL.md) を併用する。
