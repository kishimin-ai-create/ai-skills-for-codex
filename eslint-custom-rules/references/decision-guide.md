# ルール設計・AST選択ガイド

| 目的         | 主なAST/機能                                              | 注意点                                      |
| ------------ | --------------------------------------------------------- | ------------------------------------------- |
| 禁止API      | `CallExpression`、`MemberExpression`                      | alias、optional chaining、computed property |
| 命名・宣言   | `Identifier`、`VariableDeclarator`、`FunctionDeclaration` | scope、shadowing、export                    |
| JSX規約      | `JSXElement`、`JSXAttribute`                              | fragment、spread、カスタムcomponent         |
| import規約   | `ImportDeclaration`、`ExportNamedDeclaration`             | type-only、re-export、path alias            |
| TypeScript型 | parser services、型checker                                | 型情報なし設定でも安全に動作させる          |
| 自動修正     | fixer/suggestion                                          | range、コメント、format、複数修正の競合     |

ルールは「何を検出するか」と「何を修正できるか」を分離する。ASTが不足する場合に正規表現へ退行せず、parser設定または対象範囲を見直す。
