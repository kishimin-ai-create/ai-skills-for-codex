---
name: atdd-run
description: 要件定義書を入力として、PRDと受け入れ条件へ分解し、ATDDのDouble-Loopを自律的に回す。要件定義書を渡されたとき、ATDDで機能を実装してほしいと依頼されたとき、中断したATDDサイクルを再開するときに使用する。
---

# ATDD Run

要件定義書 1 つを入口として、完成まで自律的に回すための手順。

**受け入れ条件がすでに GitHub Issue にある場合は、このSkillを使わない。** `issue-loop` を使う。
`docs/ACCEPTANCE.md` を作れば、同じ受け入れ条件がIssueと文書の2か所に並び、必ず片方が古くなる。
このSkillの入口は、まだIssueへ分解されていない要件定義書である。

```text
要件定義書
    ↓  ステップ1（人間の確認あり）
docs/PRD.md ＋ docs/ACCEPTANCE.md
    ↓  ステップ2以降（AIへ委譲）
AT RED → Inner Loop → AT GREEN → 次のAC → 完了
```

## 起動方法

| 方法 | 用途 |
| --- | --- |
| `/atdd-run <要件定義書のパス>` | 対話セッションで開始する |
| `/goal <条件>` | ユーザーが入力し、条件を満たすまで自律的に回す |
| `/loop /atdd-run <パス>` | 中断した作業を一定間隔で再開する |
| 定期タスク | このSkillを呼ぶプロンプトを登録し、無人で再開する |
| `claude -p "/atdd-run <パス>" --permission-mode acceptEdits` | 無人実行 |

`/goal` と `/loop` はユーザーが入力するもので、Agentからは設定できない。

## ステップ1: 要件定義書を分解する

要件定義書を読み、次の2つへ分解する。ADR-0062 はこの2つをATDDの入力と定めている。

| 出力 | 内容 |
| --- | --- |
| `docs/PRD.md` | なぜ必要か、どのユーザー要求に応えるか、対象外は何か |
| `docs/ACCEPTANCE.md` | User Story と、それぞれの受け入れ条件（AC） |

分解であって創作ではない。要件定義書に書かれていない仕様を補ってはならない。

`acceptance-criteria-design` Skill を適用し、各ACがATへ変換できる水準かを確認する。
**AT化できないACが1つでもあれば、そこで止まり、不足している情報を質問として報告する。**
推測で埋めたACは、根拠のないATになる。

既にリポジトリが別の場所（設計文書、Issue）に受け入れ条件を持っている場合は、
どちらが優先するかを先に確認する。真実源が2系統あるまま進めない。

分解した結果はユーザーへ提示する。ここが上流工程であり、
下流をAIへ委譲できるかどうかはこの2文書の質で決まる。

## ステップ2: ATDDサイクルを回す

`atdd` Skill に従い、ACを1つずつ処理する。

1. atdd-agent へ委譲し、対象ACのATを作成させる（Outer Red）
2. ATが未実装を理由に失敗することを確認する
3. `test:` でATを確定コミットし、SHAを記録する
4. tdd-agent へ委譲し、Inner Loop（Red → Green → Refactor）を回す
5. ATを実行する。REDなら4へ戻る。GREENなら次のACへ

atdd-agent は `acceptance/` 以外を書けず、tdd-agent は `acceptance/` を書けない。
この分離はPreToolUse hookが強制する。

## ステップ3: 完了を判定する

すべてのACについて次が成立したときに完了とする。

- ATがGREEN
- Unit TestがGREEN
- lint、typecheck、format:check、buildが成功
- カバレッジの全指標が80%以上
- `acceptance/` にAT確定コミット以降の差分が無い

**判定の根拠は、実際にコマンドを実行してその出力を残すことで示す。**
「通ったはず」では根拠にならない。

## 中断と再開

中断した場合、次の情報から再開できる。

| 状態 | 判定方法 |
| --- | --- |
| どのACまで終わったか | `docs/ACCEPTANCE.md` のチェックボックス |
| ATが確定済みか | `git log -- acceptance/` |
| Inner Loopの途中か | 直近のコミットの種別（`test:` の次は `feat:`） |

再開時はステップ2の途中から入る。ステップ1をやり直さない。

## 進捗の記録

ACを1つ完了するたびに `docs/ACCEPTANCE.md` のチェックボックスを更新する。
これが中断・再開・定期実行における唯一の進捗の情報源であり、会話履歴に依存しない。

## 参照

- `atdd`: Double-Loop の手順と保護機構
- `acceptance-criteria-design`: ACがAT化できる水準かの検証
- `tdd`: Inner Loop
- [scheduling.md](./references/scheduling.md): 定期実行の選択肢と設定方法
