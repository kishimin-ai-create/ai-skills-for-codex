---
name: security-architecture
description: 依存管理、セキュアコーディング、危険機能、並行性、セキュリティログ、エラー処理をOWASP ASVSの観点で設計・実装・レビューするときに使用する。
---

# Security: Architecture and Logging

アプリケーション変更前に、依存関係、信頼境界、危険な処理、共有状態、監査要件、障害時の安全性を確認する。

## Workflow

1. 資産、攻撃面、依存関係、共有状態、ログの流れを特定する。
2. [references/security-architecture-rules.md](references/security-architecture-rules.md)から該当規則を読む。
3. 本番ビルド、入力境界、危険機能、並行処理、ログ保護、例外経路をレビューする。
4. 最小変更で制約・分離・監視・エラー境界を実装する。
5. 依存スキャン、ビルド、競合テスト、ログ形式、障害時の安全な動作を検証する。
6. 適用規則、証跡、残存リスク、未対応項目を報告する。

## Non-negotiable rules

- 依存関係は信頼できる供給元から取得し、脆弱性対応期限を管理する。
- 本番成果物へテストコード、サンプル、開発専用機能を含めない。
- 入出力フィールドと書き込み可能フィールドを明示的に許可する。
- 危険な処理を分離・隔離し、共有状態の競合とTOCTOUを防ぐ。
- ログは監査可能・機械可読・改ざん耐性を持たせ、機密情報を記録しない。
- 予期しないエラーは安全側へ倒し、fail-openやスタックトレース漏えいを許さない。

## References

- [Security architecture rules](references/security-architecture-rules.md)
