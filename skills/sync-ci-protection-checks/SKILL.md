---
name: sync-ci-protection-checks
description: GitHub Actionsのイベント別CIジョブと、mainなど共有ブランチのRuleset必須status checksを照合・更新する。PRで生成されないSmall・Medium・Largeチェックが必須になっている設定を調査し、実在する品質ゲートだけを必須にするときに使用する。
---

# Sync CI Protection Checks

## 目的

CI workflowのイベント条件と、共有ブランチ保護の必須status checksを同じ実行経路にそろえる。実行されないチェックを必須にしてPRを停止させない一方、実際に対象イベントで生成される品質ゲートは維持する。

## 手順

1. 対象リポジトリ、既定ブランチ、現在のブランチ、PRのbase/headを確認する。
2. workflowの`on`条件、job名、matrix条件、`if`、テストfilterを読み、保護対象イベントで生成されるcheck名を特定する。推測で名前を作らない。
3. GitHub Actionsの直近のworkflow runとcheck-runsを取得し、対象イベントで実際に完了したcheck名を照合する。
4. Branch ProtectionとRepository Rulesetsを読み取り、必須status checks、対象ref、enforcement、bypass actorを記録する。
5. 次の分類を行う。
   - 対象イベントで生成され成功または失敗する品質ゲート: 必須に維持する。
   - 別イベントでのみ生成されるcheck: 対象イベントの必須から外す。
   - workflowやcheck runで存在を確認できないcheck: 追加せず、原因を報告する。
6. 外部設定の変更が明示的に依頼されている場合だけ、既存Rulesetを重複作成せず最小変更する。PR必須、削除禁止、non-fast-forward禁止、bypass制限など無関係な設定は保持する。
7. 更新後にRulesetを再取得し、対象ref、enforcement、必須check一覧、bypass状態を確認する。
8. 対象PRのcheck-runsを再取得し、必須checkがすべて対象イベントで生成されることを確認する。

## 判断基準

- 「変更が進んだ側」は更新時刻ではなく、保護対象イベントで現在実際に生成されるworkflow/check-runの集合とする。Rulesetはその実行可能な集合へ合わせる。
- workflow条件とRulesetが双方で独立に変更され、意図を一意に判断できない場合は自動更新せず競合として報告する。
- PRで実行されないMediumやLargeをPRの必須checkにしない。
- テストサイズの実行時期はプロジェクトのテストサイズADRを正とする。
- 必須checkの同期はjob名の見た目ではなく、実際のworkflow条件とcheck-runの両方で検証する。
- Rulesetのbypass actorを通常運用のために追加しない。
- API権限不足で保護設定を確認・更新できない場合、変更完了とは報告しない。

## 完了報告

- 対象リポジトリと保護ブランチ
- Ruleset ID/URLとenforcement
- 変更前後の必須check一覧
- 対象イベントのworkflow run/check-run結果
- 保持した保護規則とbypass状態
- 権限エラー、未確認事項、残存リスク
