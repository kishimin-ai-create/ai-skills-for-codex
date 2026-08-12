# Scope and Exclusions

## Mutation Target

原則として、プロダクトコードをミューテーション対象とする。

以下を優先する。

1. Domain Logic
2. Business Logic
3. Validation
4. 条件分岐
5. 境界値判定
6. データ変換
7. 権限制御
8. 状態遷移
9. 金額・数値計算
10. 日付・時間処理
11. i18n の locale 判定
12. 公開対象判定
13. 広告表示条件
14. CRUD の入力検証

## Exclusion Candidates

以下は対象外候補とすることができる。

- generated code
- framework generated code
- declaration only
- type definition only
- static configuration
- migration generated code

対象外候補であっても、自動的に除外してはならない。

## Exclusion Criteria

対象外にする場合は、対象コードの性質と除外理由を確認する。

以下を除外理由として認めない。

- 重要ではないコードだから
- テストを書くのが難しい
- Mutation Score が十分高い
- ミュータントが多すぎる
- 実行時間が長い
- 対応が面倒である

## Configuration Changes

ミューテーション対象を狭める設定変更を、スコア向上だけを目的として行ってはならない。

以下の変更を行ってはならない。

- mutation 対象の不当な削減
- mutator の無効化
- exclude の追加による回避
- 対象ファイルの恣意的な除外

対象範囲を狭める必要がある場合は、人間に判断材料を提示する。

## Exclusion Record

対象外にする場合は、以下を記録する。

```text
Target:
File:
Category:
Reason:
Evidence:
Impact:
Approved By:
```

`Reason` には、対象外候補に該当する具体的な理由を記録する。

`Evidence` には、生成コード、宣言のみ、型定義のみなどと確認できる証拠を記録する。

`Impact` には、対象外によって検証されなくなる範囲を記録する。
