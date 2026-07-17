---
name: frontend-components
description: "コンポーネント設計、命名規則、コンポーネントライブラリ戦略、および保守しやすいUI構成パターン。"
---

# Frontend Components

共通UI、ドメイン固有のUI、コンポーネントの命名、フォルダ構成を設計する際に、このスキルを使用する。

## Component Categories

| Category                | Purpose                                      | Dependency on business logic | Typical owner                           | Examples                                               |
| ----------------------- | -------------------------------------------- | ---------------------------- | --------------------------------------- | ------------------------------------------------------ |
| **Common components**   | アプリ全体で利用する共通UI基盤               | 低い                         | プラットフォーム / アーキテクチャチーム | Button、Input、Dialog、Icon、Navigation                |
| **Business components** | ビジネスルールやデータを扱うドメイン固有のUI | 高い                         | 機能開発チーム                          | 商品一覧、カート概要、ユーザープロフィールウィジェット |

## Working Rules

- **表示ロジック**と**ビジネスロジック**は、可能な限り分離する。
- ビジネスUIは、本当に再利用されることが確認できた場合のみ共通パターンへ昇格させる。
- 多目的で巨大なコンポーネントよりも、小さく責務が明確なコンポーネントを優先する。

## Common Component Strategy

| Strategy                       | Use when                                             | Advantages                                                                         | Risks                                                      |
| ------------------------------ | ---------------------------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Existing component library** | 開発スピードを最優先する場合                         | 高速な開発、組み込みのアクセシビリティ、充実したドキュメント、コミュニティサポート | カスタマイズの制約、バンドルサイズ増加、ベンダーロックイン |
| **Hybrid approach**            | 必要十分な自由度を確保しつつ、一から作りたくない場合 | 開発速度と柔軟性のバランスが良い                                                   | ライブラリの学習コストと慎重な統合が必要                   |
| **Full scratch**               | 独自性の高いUI/UXが必要で、十分な技術力がある場合    | 完全な制御、高品質な成果物、ブランドに最適化しやすい                               | 開発コストが高く、継続的な保守負荷が大きい                 |

### Recommendation Order

1. 最初に**既存のコンポーネントライブラリ**を検討する。
2. ライブラリだけではスタイルや振る舞いが不足する場合は、**Hybrid approach**へ移行する。
3. **Full scratch**は、要件が明確に正当化できる場合のみ選択する。

## UI State Modeling

### Discriminated Union

UIの状態は、Discriminated Union型で明示的に表現する。

```typescript
type State =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: Data }
  | { status: "error"; message: string };
```

- 利用者と実装者の双方に対して、有効な状態を明確に表現できる
- 存在し得ない状態の組み合わせを排除できる
- 不要な条件分岐を減らせる

### JSX Structure as UI State

Discriminated Unionが複雑になりすぎる場合は、JSXの構造自体でUI状態を表現する。

- Loading状態 → `<Suspense fallback={...}>`
- Error状態 → `<ErrorBoundary fallback={...}>`

Propsだけではなく、コンポーネント境界によってUI状態を表現する。

## Suspense Boundary

`<Suspense>` はReactの仕組みであり、非同期処理（データ取得やLazy Importなど）が完了するまでコンポーネントツリーの描画を待機し、その間は `fallback` を表示する。

### When to use Suspense

- Lazy Loadingされたコンポーネント（`React.lazy(() => import(...))`）
- Suspense対応のデータ取得ライブラリ（React Queryの `suspense: true`、Relay、Next.js Server Components）
- ルート単位または機能単位のコード分割

### Placement rules

- `<Suspense>` は**非同期処理にできるだけ近い位置**へ配置する。ページ全体ではなく、対象コンポーネントだけを囲むことで、細かなローディング表示が可能になる。
- 予期しないSuspensionへの最終防衛線として、ルートレベルにも `<Suspense>` を配置する。
- ローディングとエラーの両方を扱うため、`<ErrorBoundary>` を `<Suspense>` の直上に配置する。
- プロジェクト固有のUI仕様を確認してからローディング状態を変更する。初回ページロードでは仕様に定めた全画面またはページ単位の表示を使い、一覧の再取得やフォーム送信時は対象範囲のみローディング表示を行う。

```tsx
<ErrorBoundary fallback={<ErrorMessage />}>
  <Suspense fallback={<Spinner />}>
    <UserProfile userId={id} />
  </Suspense>
</ErrorBoundary>
```

### Anti-patterns

- ページ全体を1つの `<Suspense>` で囲むこと。1つのセクションだけが読み込み中でもページ全体がスピナー表示になる。
- Suspense非対応のデータ取得（`useEffect` + `useState` など）と組み合わせること。期待どおり動作しない。
- `<Suspense>` と一緒に `<ErrorBoundary>` を配置しないこと。Suspension中に発生したエラーを処理できない。

## Useful Patterns

再利用性や拡張性が向上する場合は、既存のデザインパターンを活用する。

- Factory pattern
- Module pattern
- Compound components
- Higher-order components
- Render props

流行だから採用するのではなく、重複削減や責務の明確化につながる場合のみ採用する。

## List UI Contracts

- ページネーションは、対象一覧の契約の一部として扱い、`page`、`pageSize`、`totalCount`、`onPageChange` を常にセットで扱う。
- ページネーション状態は、APIクエリを管理するページまたはルートレベルのコンテナで保持する。
- 日付などのフィルターが変更された場合は、`page` を `1` にリセットする。
- ラベルや動作が同じであれば、複数の画面や機能で同じページネーションコンポーネントを再利用する。
- APIから `totalCount` を取得しているにもかかわらず、ユーザーが操作できる前後ページのUIを表示しない実装は行わない。

## i18n UI Contracts

- 特定ロケールやデフォルトロケールのメッセージオブジェクトを、描画時のフォールバックとして直接読み込まない。
- ローディング表示は `useTranslations` を利用するコンポーネント経由で描画し、テキストやロゴの代替テキストが現在のロケールに従うようにする。
- アプリ内で言語切り替えを提供する場合、ブラウザタブのサービス名も選択中のロケールと一致させる。
- favicon横に表示されるタイトルもUIの一部として扱い、デフォルト言語のまま放置しない。

## Naming Conventions

| Target                     | Convention   | Example                 |
| -------------------------- | ------------ | ----------------------- |
| Component file / class     | `PascalCase` | `UserProfileCard.tsx`   |
| Props / events / variables | `camelCase`  | `onSubmit`, `isLoading` |
| CSS classes / folder names | `kebab-case` | `user-profile-card`     |

### Naming Rules

- コンポーネントの役割が分かる名前を付ける。
- ドメイン固有のコンポーネントでは、ドメイン用語を優先する。
- 分かりにくい略称や曖昧な名前は避ける。

```text
Good:
- ButtonPrimary
- InputSearch
- UserProfileCard
- OrderListItem

Avoid:
- BtnX
- DataBox
- InfoThing
```

## Design Principles

### 1. Modularity and Encapsulation

- 各コンポーネントには明確なインターフェースと責務を持たせる。
- 実装の詳細はPropsやイベントの背後に隠蔽する。
- コンポーネント変更時の意図しない副作用を減らす。

### 2. Reusability

- パラメータ化やCompositionによって、複数の利用場面へ適応できるようにする。
- 再利用は、一貫性を生むために行い、不必要な結合を生まないようにする。

### 3. Maintainability

- コンポーネントは小さく保つ。
- 一貫した命名規則とコーディング規約に従う。
- デバッグしやすく、変更影響が分かりやすい構造にする。

### 4. Extensibility

- 小さなコンポーネントを組み合わせて複雑なUIを構築する。
- 深い継承よりCompositionを優先する。
- Micro Frontendは、組織規模が必要性を生む場合のみ検討する。

## Common Anti-Patterns

| Anti-pattern                      | Why it hurts                                               | Better approach                                      |
| --------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------- |
| **God Object component**          | 単一責任の原則を破り、テスト・変更が困難になる             | 責務ごとの小さなコンポーネントへ分割する             |
| **Tight coupling**                | 一箇所の変更が他の機能へ波及する                           | 安定したインターフェースやDI、イベント駆動を利用する |
| **Magic numbers**                 | 意味が分かりにくく保守しづらい                             | 名前付き定数や設定値へ置き換える                     |
| **Over-engineering**              | 開発コストと実行コストを増やす                             | 現在の課題を最も単純な方法で解決する                 |
| **Ignoring accessibility**        | 利用できないユーザーが生まれ、後からの修正コストも高くなる | 最初からWCAGと支援技術への対応を組み込む             |
| **Mixing business logic into UI** | UIの再利用性とテスト性が低下する                           | ビジネスロジックをService、Hook、Moduleへ移動する    |
| **Inconsistent styling**          | UXの一貫性が失われる                                       | スタイルガイドと統一したスタイリング戦略を利用する   |
| **Ambiguous link labels**         | アクセシビリティと分かりやすさを損なう                     | 内容が分かるリンクラベルを使用する                   |
| **Tiny click targets**            | モバイルで操作しづらい                                     | 十分な余白とタップ領域を確保する                     |

## Suggested Directory Structures

### Small Project

```text
src/
├── core/
│   └── services/
├── shared/
│   └── components/
├── features/
│   ├── dashboard/
│   │   └── components/
│   └── users/
│       └── components/
└── assets/
```

### Large Project

```text
src/
├── app/
├── features/
│   ├── products/
│   │   ├── components/
│   │   ├── schemas/
│   │   └── server/
│   └── users/
│       ├── components/
│       └── server/
├── lib/
├── api/
├── database/
├── components/
└── utils/
```

## Default Recommendation

- まず**フレームワーク標準の規約**に従う。
- **アプリ全体で共有するUI**と**機能ごとに所有するUI**を明確に分離する。
- 抽象化は、実際に繰り返し利用されることが確認できてから導入する。
