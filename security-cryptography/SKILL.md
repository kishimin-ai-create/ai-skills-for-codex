---
name: security-cryptography
description: 暗号アルゴリズム、ハッシュ、暗号学的乱数、鍵管理、暗号アジリティを設計・実装・レビューするときに使用する。OWASP ASVS 5.0 V11を扱う。
---

# Security: Cryptography

暗号処理を変更するときは、保護対象、鍵の用途、脅威、ライフサイクルを確認し、詳細規則を [references/security-cryptography-rules.md](references/security-cryptography-rules.md) から該当範囲だけ読む。

## Workflow

1. 暗号化、ハッシュ、署名、乱数、鍵、証明書の用途とデータフローを特定する。
2. 使用ライブラリ、アルゴリズム、鍵長、nonce/IV生成、保存場所、ローテーションを確認する。
3. V11の該当規則を適用し、実績のある暗号ライブラリを使用する。
4. 最小変更で実装し、鍵素材・平文・エラー詳細が漏えいしないことを確認する。
5. 正常系、改ざん、鍵不一致、期限切れ、乱数、失敗時の安全性をテストする。
6. 採用アルゴリズム、鍵ライフサイクル、検証結果、移行計画、残存リスクを報告する。

## Non-negotiable rules

- 自作暗号プリミティブを実装せず、業界で検証されたライブラリを使用する。
- ECB、MD5、SHA-1をセキュリティ用途に使わず、認証付き暗号化と衝突耐性のあるハッシュを選ぶ。
- セキュリティ用途の乱数にはCSPRNGを使用し、`Math.random()`を使わない。
- nonce/IVを同一鍵で再利用せず、鍵素材をソース、ビルド成果物、通常の設定へ保存しない。
- 暗号処理は定時間性と安全な失敗を保ち、パディングオラクルなどの情報を漏らさない。

## References

- [Security cryptography rules](references/security-cryptography-rules.md)
- 秘密情報の保管・ローテーションは [security-config](../security-config/SKILL.md)、パスワード・認証は [security](../security/SKILL.md) も併用する。
