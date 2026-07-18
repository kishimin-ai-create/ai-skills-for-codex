---
name: backend-patterns
description: バックエンドのDDD・Clean Architecture、ModelからControllerまでの実装順序、Repository境界、エラー変換、テスト戦略と検証を行うときに使う。言語・フレームワーク固有の規則は対象リポジトリへ適応する。
---

# Backend Patterns

バックエンド変更では、対象リポジトリの`AGENTS.md`、ADR、既存構成を先に確認し、このSkillの境界規則を適用する。特定の言語・フレームワークの規約はリポジトリ側の指示を優先する。

## Implementation workflow

1. 作業ディレクトリを確認し、バックエンドのビルド・型検査・テスト設定を読む。
2. バックエンドに関連するADRとリポジトリのBackend指示を先に読む。UI専用の設計文書はBackend作業の参照対象にしない。ユーザーHOME配下の参照は`$HOME`表記を使う。
3. 次の順序でレイヤーを設計・実装する。各段階でRed → Green → Refactorを適用する。

| 順序 | レイヤー       | 作業                                                              |
| ---- | -------------- | ----------------------------------------------------------------- |
| 1    | Model          | Domain entity、Value Object、business ruleを定義する              |
| 2    | Repository     | Model側にRepository interface（Port）を定義する                   |
| 3    | Service        | Repository interfaceを使ってUsecaseを実装する                     |
| 4    | Infrastructure | DB、外部API、adapterなどの実装詳細を追加する                      |
| 5    | Controller     | Request/responseを処理し、Serviceへ委譲する                       |
| 6    | Test           | Model → Service → Infrastructure → Controllerの順で契約を検証する |

この順序によりDomainのframework結合を防ぎ、Repository interfaceを先に定義してServiceを外部依存なしで検証できる。

4. 外側の層から内側の層へ契約を越える場合は、Domainの型・Port・エラー境界を確認する。
5. テストは対象の隣または機能境界に置き、リポジトリが定義する命名・実行規則に従う。
6. 変更後はリポジトリが定義するlint、型検査、testを実行し、未実行の検証を報告する。

## 必須設計規則

- Modelは他レイヤーに依存せず、framework、DB、HTTPを参照しない。
- Serviceは業務ロジックとUsecaseのオーケストレーションを担い、DB・HTTPなどInfrastructure詳細を含めない。
- RepositoryのInterfaceはModel側、実装はInfrastructure側に置く。Infrastructure固有エラーを漏らさない。
- Controllerは薄く保ち、リクエスト解析、Service呼び出し、レスポンス変換だけを行う。
- InfrastructureはDB、外部API、frameworkなど外部システムを扱い、業務ロジックを持たない。
- 依存は内側（Model）へ向け、内側の層から外側の層を参照しない。
- Infrastructureエラーは境界を越える前にDomain固有の型へ変換する。

詳細な構造・依存ルールは[references/architecture.md](references/architecture.md)を読む。

## テスト規則

- リポジトリがサイズ接尾辞（例: `.small.test.ts`、`.medium.test.ts`、`.large.test.ts`）を定義している場合は使用する。
- `unit`と`integration`はテスト意図の説明にのみ使う。
- テストは対象の隣または機能境界へ配置し、既存リポジトリが定義する配置規則がある場合はそれを優先する。
- 各リソースは専用ファイルに分け、共有要素は最も近い共通テスト境界へ置く。

詳細なテストレベル、配置、実行順は[references/testing.md](references/testing.md)を読む。

## Testing strategy

- システムを理解してからテストを設計する。
- 実装詳細ではなく、利用者から観測できる振る舞いで品質を定義する。
- 影響度と発生可能性が高いリスクからテストを優先する。
- 複雑なフローでは自動テストと探索的テストを組み合わせる。
- テスト本体はArrange → Act → Assertを基本構造とする。
- テストしにくいUnitは責務過多の兆候として設計を見直す。
- 複雑で保守しにくいセットアップは設計上の問題として扱う。

テストサイズ、範囲、DB利用、Playwrightなどの具体的な適用条件は[references/testing.md](references/testing.md)へ集約する。

## Security boundary

認証、パスワード、トークン、秘密情報、入力境界の詳細は[`$HOME/.agents/security/SKILL.md`](../security/SKILL.md)を参照し、Backend Skillへ重複記載しない。

## コマンド

作業対象のpackage scriptsとリポジトリ指定のシェルを優先し、存在しないコマンドや特定ツールを推測しない。指定がない場合はバックエンドディレクトリで、lint、型検査、テストをこの順に実行する。

```bash
<repository-lint-command>
<repository-typecheck-command>
<repository-test-command>
```

検証が失敗した場合は実装、テスト、環境の原因を分離する。

## 完了報告

変更したレイヤーと依存方向、テスト配置、実行したコマンドと結果、未実行の検証、残存リスクを簡潔に報告する。仕様にない機能、外側への依存、raw Infrastructure errorの漏出を追加していないことを確認する。
