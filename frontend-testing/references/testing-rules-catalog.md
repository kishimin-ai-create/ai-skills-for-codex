---
name: frontend-testing
description: フロントエンドテストの命名、Arrange・Act・Assert構造、セマンティッククエリの優先順位、スナップショットの範囲を統一するためのテスト実装ルール。
---

# Frontend Testing

## 目的

フロントエンドテストを、期待する振る舞いが明確で読みやすく、実装詳細に依存しない形で記述すること。

## 手順

### 1. テスト名を記述する

テスト名では、以下を表現する。

- 何をテストするのか
- どのような条件で
- どのような結果を期待するのか

### 2. Arrange / Act / Assert で構成する

すべてのテスト本体を **Arrange / Act / Assert（AAA）** の構造にする。

### 3. クエリの優先順位が高いものを使用する

クエリは以下の優先順位で使用する。

#### 1. Queries Accessible to Everyone

1. `getByRole`
2. `getByLabelText`
3. `getByPlaceholderText`
4. `getByText`
5. `getByDisplayValue`

#### 2. Semantic Queries

1. `getByAltText`
2. `getByTitle`

#### 3. test-id

1. `getByTestId`

`getByTestId` は最後の手段としてのみ使用する。
`getByTestId`を使用する時はコメントを追加する

### 4. スナップショットの範囲を限定する

スナップショットは小さく、対象を絞ったものにする。

大規模または過度に詳細なスナップショットを作成してはならない。

## 参照

フロントエンドのテストの実装を行う時に下記を必ず参照しなさい。

- [guiding-principles.md](./references/guiding-principles.md)
