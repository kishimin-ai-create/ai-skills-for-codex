---
name: security-authn
description: パスワード、MFA、認証、セッションToken、Timeout、Logout、セッション終了、アカウント保護をOWASP ASVSの観点で設計・実装・レビューするときに使用する。
---

# Security: Authentication and Session

認証・セッションを変更する前に、認証要素、脅威モデル、Tokenの所有者、失効経路、再認証条件、管理者操作を確認する。

## Workflow

1. 対象ユーザー、認証方式、回復フロー、Sessionの状態と信頼境界を特定する。
2. [references/security-authn-rules.md](references/security-authn-rules.md)から該当規則を読む。
3. Password、MFA、Credential Recovery、Session Token、Timeout、Logout、Step-upを設計する。
4. BackendでToken、失効、認可、Rate Limit、Anti-automationを検証する。Clientだけで検証しない。
5. 正常系、失敗系、Brute Force、Credential Stuffing、Session Hijacking、失効、再認証をテストする。
6. 採用した認証強度、Timeout値、失効条件、検証結果、残存リスクを報告する。

## Non-negotiable rules

- パスワードを勝手に切り詰めず、許可された長さ・文字をそのまま検証する。
- MFA、認証回復、Session Tokenの安全性をログインと同等以上に保つ。
- Session TokenはCSPRNGで生成し、Backendで検証・失効する。
- Logout、Expiration、Password/MFA変更、アカウント無効化時の失効経路を実装する。
- Idle TimeoutとAbsolute Timeoutを設定し、値と根拠を文書化する。
- 機密属性の変更や高リスク取引には再認証またはStep-up認証を要求する。

## References

- [Security authentication rules](references/security-authn-rules.md)
