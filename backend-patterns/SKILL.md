---
name: backend-patterns
description: 言語・フレームワークに依存せず、バックエンドのDDD・Clean Architecture、依存方向、Repository境界、エラー変換、テスト設計と検証を行うときに使う。
---

# Backend Patterns

バックエンド変更では、対象リポジトリの`AGENTS.md`、ADR、既存構成を先に確認し、このSkillの境界規則を適用する。特定の言語・フレームワークの規約はリポジトリ側の指示を優先する。

## クイックワークフロー

1. 作業ディレクトリを確認し、バックエンドの実際のビルド・型検査・テスト設定を読む。
2. バックエンドに関連するADRとリポジトリのBackend指示を先に読む。UI専用の設計文書はBackend作業の参照対象にしない。ユーザーHOME配下の参照は`$HOME`表記を使う。
3. レイヤー（Model、Service、Repository、Controller、Infrastructure）と依存方向を図にしてから変更する。
4. 外側の層から内側の層へ契約を越える場合は、Domainの型・Port・エラー境界を確認する。
5. テストは対象の隣または機能境界に置き、リポジトリが定義する命名・実行規則に従う。
6. 変更後はバックエンドディレクトリでlint、typecheck、testを実行し、未実行の検証を報告する。

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
