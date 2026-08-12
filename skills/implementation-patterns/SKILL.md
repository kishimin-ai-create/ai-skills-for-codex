---
name: implementation-patterns
description: 既存テストと契約を満たす最小実装を導く。Greenフェーズ、テスト駆動のバックエンド実装、テストからのUI実装、テストが期待動作を定義する不具合修正で使用する。
---

# Implementation Patterns

テストまたは明示された契約が期待動作を定義した後に使用する。

## Workflow

1. 失敗中または追加されたテストと、関連するDomain/API契約を読む。
2. 成功、入力検証、業務上の競合、境界値、Infrastructure障害、副作用など観測可能な要件を抽出する。
3. [references/implementation-catalog.md](references/implementation-catalog.md)から最小のパターンを選ぶ。
4. テストと契約が要求する振る舞いだけを実装する。
5. Red → Green → Refactorサイクルを維持し、Greenフェーズでリファクタリングしない。
6. 対象テストを先に実行し、その後リポジトリ全体の検証コマンドを実行する。

## Guardrails

- テストが検証する正確なレスポンス形式、ステータスコード、エラーコード、メッセージを維持する。
- Infrastructure呼び出しや業務ルールより先に入力を検証する。
- Infrastructure障害を公開エラー契約へ変換し、内部情報を漏えいさせない。
- 誤った実装を通すためにテストを変更しない。
- 完全性を理由に、未テストの機能、ページネーション、抽象化、ヘルパー、ログ、コメントを追加しない。
- テストが実際の振る舞いを要求している場合、拒否結果をハードコードしない。
- 言語・フレームワーク固有の詳細は対象リポジトリの規約に従う。カタログの例は説明用である。

## References

- [実装パターンカタログ](references/implementation-catalog.md)
