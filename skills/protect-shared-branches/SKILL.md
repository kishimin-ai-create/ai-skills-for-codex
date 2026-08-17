---
name: protect-shared-branches
description: GitHubなどの共有Gitリポジトリでmain・release等への直接pushを、サーバー側Rulesetとローカルpre-push hookの二段階で防止・検証する。直接push事故、誤ったupstream、HEAD:main refspec、ブランチ保護、PR必須化、bypass禁止を扱うときに使用する。
---

# Protect Shared Branches

共有履歴の所有者であるサーバーを最終防壁とし、ローカルhookを早期検出に使う。注意喚起、AGENTS.md、Skill、hookだけを最終防壁にしない。

## 手順

1. リポジトリ、既定ブランチ、共有ブランチ、現在のRuleset、権限、CI check名、ローカルhookを読み取りで確認する。
2. 現在ブランチのupstreamが共有ブランチを指していないか確認する。誤設定は報告し、変更依頼がある場合だけ修正する。
3. 外部変更の許可を確認してから、共有ブランチを対象とするActiveなサーバー側Rulesetを作成または更新する。
4. Rulesetへ次を設定する。
   - Pull Requestを必須にする。
   - 実在を確認したCI status checksを必須にする。
   - 削除とnon-fast-forward更新を禁止する。
   - 通常運用のbypass actorを設定しない。
5. [install-pre-push-hook.ps1](scripts/install-pre-push-hook.ps1)でローカルhookを設定する。既存の管理外hookは上書きせず停止する。
6. 疑似入力で共有ブランチ宛てが失敗し、作業ブランチ宛てが成功することを確認する。
7. サーバーからRulesetを再取得し、Active、対象ref、規則、必須check、bypass状態を確認する。

## Rulesetの安全条件

- branch targetを共有ブランチまたは既定ブランチへ限定する。
- 必須check名を推測しない。直近のworkflow runまたはcheck runから取得する。
- bypassが必要な緊急運用は通常設定へ混ぜず、別の明示的な判断として扱う。
- Ruleset作成・更新に失敗した場合、ローカルhookだけで保護完了と報告しない。
- 既存Rulesetがある場合、重複作成せず内容と適用範囲を比較する。

## ローカルhookの位置付け

- hookは送信前に分かりやすく失敗させる補助防壁である。
- `.git/hooks`はcloneごとに異なるため、再clone後は再設定する。
- hookが存在しても、サーバー側Rulesetの検証を省略しない。

## 完了報告

- repository、保護対象、Ruleset ID/URL、enforcement、規則、必須check、bypass状態を示す。
- hookの保存先と共有ブランチ拒否・作業ブランチ許可の検証結果を示す。
- upstream誤設定、再clone時のhook再設定、未定義の緊急復旧手順などの残存リスクを示す。

