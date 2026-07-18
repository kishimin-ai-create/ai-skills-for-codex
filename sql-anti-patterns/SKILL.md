---
name: sql-anti-patterns
description: SQLスキーマ、クエリ、インデックス、外部キー、トランザクションのアンチパターンを検出し、安全性・整合性・性能を保つ改善案を設計するときに使用する。
---

# SQL Anti-patterns

## Workflow

1. 対象DBMS、バージョン、スキーマ、制約、データ量、実行計画、トラフィックを確認する。
2. [references/sql-anti-pattern-catalog.md](references/sql-anti-pattern-catalog.md)から該当する分類を選ぶ。
3. 可用性、整合性、セキュリティ、性能、保守性への影響を分離して評価する。
4. 既存データ、ロック、オンライン変更、ロールバックを考慮して最小の改善案を作る。
5. 改善後の制約、クエリ結果、実行計画、負荷、権限、マイグレーションを検証する。
6. アンチパターン、根拠、改善案、トレードオフ、未検証の前提を報告する。

## Non-negotiable rules

- SQLは必ずパラメータ化し、文字列連結で入力を埋め込まない。
- パスワードや秘密情報を平文で保存しない。
- 外部キー、UNIQUE、CHECK、NOT NULLなど、データ整合性をDB制約で表現する。
- `SELECT *`、無制限取得、不要なN+1、暗黙の型変換、非SARGableな条件を無批判に追加しない。
- インデックスはクエリ、選択性、書き込みコスト、実行計画を根拠に追加する。
- トランザクション境界、分離レベル、ロック、リトライ、冪等性を明示する。
- DBMS固有の挙動を移植可能と推測しない。対象DBMSの仕様を優先する。

## Review output

報告には、該当パターン、影響、再現クエリまたは実行計画、改善SQL・マイグレーション、データ移行手順、検証結果、残存リスクを含める。

## References

- [SQL anti-pattern catalog](references/sql-anti-pattern-catalog.md)
