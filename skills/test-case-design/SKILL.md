---
name: test-case-design
description: 要件・仕様・既存コードから、振る舞いを網羅するテストケース、test.todo計画、Small・Medium・Large別のテストファイル、実装済みテスト、回帰検証を設計・レビューするときに使用する。
---

# Test Case Design

テストを観測可能な振る舞い・事後条件・不変条件として設計する。対象言語、テストランナー、実行コマンドを先に検出し、ツールをSkillへ固定しない。

## 手順

1. 要件、受入条件、公開API、エラー契約、既存テスト、ADR、境界（HTTP・DB・時刻・乱数）を収集する。
2. 正常、代替、境界、異常、権限、再試行、競合、空・遅延状態を状態表にする。各ケースに入力、操作、期待結果、検証対象、根拠を付ける。
3. Unit/Component/Integration/Contract/E2Eのどの層が最小コストで契約を証明するか選び、`test-sizes`に従ってSmall、Medium、Largeを決める。重複する同一観測を複数層へ無計画に複製しない。
4. リポジトリ規則に従ってサイズをファイル名、クラス名、タグまたはディレクトリへ明示する。規則がなければC#は`SubjectSmallTests.cs`、TypeScriptは`subject.small.test.ts`を基準とし、異なるサイズを同じファイルへ混在させない。
5. 未実装ケースは`describe`/`it`の名前で意図を表す`test.todo`にする。各`test.todo`の直前に、`// ID`、`// Source`、`// Given`、`// When`、`// Then`、必要な`// Error`または`// Blocked by`、`// Priority`をこの順で書く。コメントを`describe`の先頭やファイル末尾へまとめない。todoを成功扱いにしない。
6. 実装時は利用者向けの入力・出力・副作用を検証し、内部実装や脆いDOM構造を直接固定しない。副作用は境界で制御する。
7. 失敗時は期待値、実測値、再現条件、分類（実装・テスト・環境・仕様）を記録し、推測を原因として断定しない。
8. 実行コマンド、結果、未実行項目、残存リスク、要件との対応表を出力する。

## 網羅性

- 入力：最小、代表、最大、空、null、型不正、特殊文字、長文、ロケール。
- 状態：初期、loading、success、empty、error、retry、cancel、disabled、権限不足、競合。
- 時系列：初回、再実行、連打、並行要求、古い応答、再接続、タイムアウト。
- 不変条件：データ損失なし、重複副作用なし、認可境界、 idempotency、順序、フォーカス。

## `test.todo` scaffold contract

- コメントは対象の`test.todo`へ隣接させ、別ケースとの対応を曖昧にしない。
- `ID`はファイル内で一意かつ安定した識別子にする。
- `Source`には要件、仕様、ADR、API契約、または回帰元を記載する。
- `Given`、`When`、`Then`は実装詳細ではなく、入力条件、利用者の操作、観測可能な結果を書く。
- `Error`は期待する失敗契約がある場合、`Blocked by`は実装や仕様決定を待つ場合に書く。該当しない項目を捏造しない。
- `Priority`は`P0`、`P1`、`P2`のいずれかとし、`test.todo`名へ重複して埋め込まない。
- 計画段階ではassertion、fixture、fake、stub、データプロバイダー、プロダクションコードを追加しない。

## 参照

- [テストレベル選択](references/test-levels.md)
- [Vitest/Jestパターン](references/vitest-patterns.md)
- [レビュー基準](references/review-checklist.md)

## 出力契約

テスト一覧、各ケースのサイズ、作成・変更したサイズ別ファイル、`test.todo`一覧、層とサイズの選択理由、実行結果、未検証条件、残存リスクを簡潔に報告する。
