---
name: eslint-custom-rules
description: JavaScript・TypeScriptの決定的な規約をカスタムESLintルールとして設計・実装・テスト・導入・移行するときに使用する。
---

# Custom ESLint Rules

繰り返すレビュー指摘を、明確なAST上の契約と安全な自動検査へ変換する。型検査・formatter・runtime validationで解くべき問題を無理にESLintへ移さない。

## 設計手順

1. 規約、違反例、許可例、対象ファイル、例外、移行期限、失敗時の影響を文章で確定する。
2. 既存のcore/plugin rule、TypeScript型検査、formatterで代替できないか調査する。ルール名とseverity、適用config、ownerを決める。
3. parser・sourceType・JSX・TypeScriptのASTノードとscopeを確認し、文字列検索や脆い位置判定に依存しない。
4. `create`からvisitorを登録し、最小の違反ノードで一度だけ`context.report`する。メッセージ、位置、suggestionを利用者が修正できる形にする。
5. 修正が決定的で安全な場合だけ`fix`またはsuggestionを実装する。意味を変える修正、複数解釈、コメント・format破壊の可能性がある場合は自動修正しない。
6. RuleTesterでvalid/invalid、複数違反、境界、parserOptions、TypeScript型情報の有無、fix outputをテストする。ルール自身のテストを最初に失敗させてから実装する。
7. plugin export、flat config/legacy config、recommended設定、severity、ignore、monorepo対象を確認し、段階的にwarningからerrorへ移行する。
8. 型検査、Lint対象、rule test、全体Lint、buildを実行し、違反数・自動修正差分・未適用ファイルを報告する。

## 判断基準

- 決定的で機械的な規約はルール化する。
- 意味理解・設計判断・外部情報を要する規約はレビューや別ツールへ残す。
- false positiveを減らすため、対象構文を狭く始め、明示的な例外と理由を設ける。
- `eslint-disable`は最小範囲に限定し、理由と期限またはissueを記録する。
- rule変更は既存違反の件数、CI時間、開発者の修正負荷を評価して移行する。

## 参照資料

- [ルール設計・AST選択ガイド](references/decision-guide.md)
- [実装・レビュー checklist](references/review-checklist.md)

## 出力契約

規約、対象AST、valid/invalid例、報告メッセージ、fix方針、RuleTesterケース、設定変更、移行計画、検証結果、残存リスクを報告する。
