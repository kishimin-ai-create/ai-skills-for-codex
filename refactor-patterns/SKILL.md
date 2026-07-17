---
name: refactor-patterns
description: TypeScriptコードのリファクタリングパターン集。RefactorAgentが参照する詳細なパターン例、アンチパターン、実装例をまとめる。
---

# Refactoring Patterns

## Common Refactoring Patterns

### Pattern 1: Extract Validation Logic (No Behavior Change)

入力検証をビジネスロジックから分離し、専用のメソッドへ抽出する。

**Why safe**

- 戻り値が同一である
- エラーコードが変わらない
- 処理の流れが維持される

### Pattern 2: Extract Error Response Factory (Eliminate Duplication)

重複しているエラーレスポンス生成処理を、共通のメソッドへまとめる。

**Why safe**

- 戻り値が同一である
- エラーコードが変わらない
- データ構造が変わらない

### Pattern 3: Rename for Clarity (Preserves All Behavior)

変数、メソッド、クラスを、役割が分かりやすい名前へ変更する。

**Why safe**

- ロジックが変わらない
- 振る舞いが同一である
- 名前だけを変更するため、既存のテスト結果に影響しない

### Pattern 4: Guard Clauses (Improved Readability, No Behavior Change)

ネストした条件分岐を早期リターンへ変更する。

**Why safe**

- 制御フローが同一である
- 戻り値が変わらない
- ロジックの意味が維持される

### Pattern 5: Consolidate Similar Error Handling

重複しているエラーハンドリングを統合する。

**Why safe**

- エラー処理の経路が同一である
- 戻り値が変わらない
- 振る舞いが維持される

## Specific Refactoring Techniques for Backend (Hono + TypeScript)

### Technique 1: Extract Port/Adapter Responsibilities

- Repository固有の処理をRepositoryクラスへ移動する
- バリデーションをValidatorクラスまたは関数へ移動する
- Interactorにはオーケストレーションだけを残す

### Technique 2: Improve Error Handling in Service Layer

- `try-catch` のパターンを統合する
- インフラストラクチャのエラーをドメインエラーへ一貫して変換する
- エラーレスポンスの生成処理を抽出する

### Technique 3: Organize Usecase Classes

- Interactorごとに公開メソッドを `execute` の1つだけにする
- サブ責務をprivateメソッドへ分離する
- 入力検証、ビジネスロジック、エラーハンドリングを明確に分離する

## Specific Refactoring Techniques for Frontend (React + TypeScript)

### Technique 1: Extract Components (No Behavior Change)

複数の責務を持つ大きなコンポーネントを、責務ごとのコンポーネントへ分割する。

### Technique 2: Extract Custom Hooks (No Behavior Change)

コンポーネント内の状態管理や共通ロジックをCustom Hookへ分離する。

### Technique 3: Improve Prop Handling (No Behavior Change)

意味が分かりにくいPropsを、意図が明確なPropsへ変更する。

## Anti-Patterns: Things That Look Safe But Aren't

### Anti-Pattern 1: "Just Optimizing" (Without Clarity Improvement)

可読性を改善せず、パフォーマンスの向上だけを目的として変更する。

**Why risky**

最適化だけを目的とした変更は、振る舞いの違いを隠す可能性がある。保守的に変更する。

### Anti-Pattern 2: "Better Organization" (Changing Behavior)

コードを整理する過程で、バリデーションやデータベースアクセスなどの処理順序を変更する。

**Why risky**

処理順序の変更は、データベース呼び出しの有無など、外部から観測可能な振る舞いに影響する可能性がある。

### Anti-Pattern 3: "Adding Comments for Future Devs"

リファクタリングの一部として、説明コメント、TODO、lint無効化などを追加する。

**Why risky**

リファクタリングに本来必要のない変更が含まれ、変更範囲や意図が不明確になる。

### Anti-Pattern 4: "Fixing Supposed Bugs" While Refactoring

リファクタリングと同時に、想定上の不具合を修正する。

**Why risky**

既存テストが定義している振る舞いを変更する可能性がある。不具合を修正する場合は、先に失敗するテストを追加する。

## Safety-First Example: CreateAppInteractor Refactoring

安全なリファクタリングでは、次のような改善を行う。

- 入力検証を専用メソッドへ抽出する
- エラーレスポンスの生成処理を共通化する
- 成功レスポンスの生成処理を共通化する
- 変数やメソッドの名前を明確にする
- ガード節を使用して可読性を向上させる

**Why This Refactoring is Safe**

- すべてのテストが成功する
- 外部から観測できる振る舞いが同一である
- 戻り値とエラーコードが変わらない
- バリデーションロジックが明確になる
- エラーハンドリングの重複が削減される
- Repository呼び出しなどの副作用が維持される
- 新しい機能を追加していない
