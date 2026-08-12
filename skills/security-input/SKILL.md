---
name: security-input
description: 入力のエンコード、出力エスケープ、インジェクション防止、サニタイズ、サーバー側検証、業務フロー、ファイル処理を設計・実装・レビューするときに使用する。OWASP ASVS 5.0 V1・V2・V5を扱う。
---

# Security: Input

入力境界を変更するときは、入力元、解釈されるコンテキスト、信頼境界、出力先を特定し、詳細規則を [references/security-input-rules.md](references/security-input-rules.md) から該当範囲だけ読む。

## Workflow

1. 入力の種類、形式、サイズ、利用先（HTML、SQL、OS、URL、ファイルなど）を洗い出す。
2. デコード、検証、サニタイズ、出力エンコードの順序と実行層を確認する。
3. V1/V2/V5の該当規則を適用し、許可リストと上限を定義する。
4. 最小変更で実装し、クライアント検証だけに依存せず、信頼されたサーバー側境界で拒否する。
5. 正常系、境界値、インジェクション、業務フロー逸脱、過剰サイズ、ファイル爆弾をテストする。
6. 適用規則、検証結果、拒否条件、未確認事項、残存リスクを報告する。

## Non-negotiable rules

- 入力は一度だけデコードし、検証後に再度アンエスケープしない。出力エンコードはインタープリターへ渡す直前に行う。
- SQL、OS、LDAP、XPath、テンプレートなどへ入力を連結せず、パラメーター化またはコンテキスト別エンコードを使う。
- クライアント側検証をセキュリティ制御とみなさず、サーバー側で型・形式・範囲・長さを許可リスト検証する。
- `eval()`や危険なデシリアライズを避け、SSRF、ReDoS、XXE、パストラバーサルを防ぐ。
- アップロードは拡張子だけで信頼せず、内容、サイズ、個数、展開後容量、実行可否を検証する。

## References

- [Security input rules](references/security-input-rules.md)
- 認証境界は [security](../security/SKILL.md)、ブラウザ描画は [security-frontend](../security-frontend/SKILL.md)、API通信は [security-api](../security-api/SKILL.md) を併用する。
