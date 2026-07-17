---
name: frontend-state
description: "状態の分類、保存先の選択、サーバーキャッシュのパターン、オフライン対応可能なデータ管理。"
---

# Frontend State

UI状態、共有アプリケーション状態、サーバーデータ、オフラインデータの保存方法を選定する際に、このスキルを使用する。

## Start by Classifying State

| State type            | Scope                                                  | Typical examples                          | Default home                          |
| --------------------- | ------------------------------------------------------ | ----------------------------------------- | ------------------------------------- |
| **UI state**          | 単一コンポーネントまたはローカルなコンポーネントツリー | Modalの開閉、Tab、Form入力、並び順        | Component state、Hooks、Local context |
| **Application state** | アプリ全体で共有                                       | 現在のUser、Theme、App設定、Global filter | Contextまたは軽量なGlobal store       |
| **Server state**      | Backendと同期                                          | API Response、Master data、Transaction    | Cacheを備えたServer-state library     |

## Local State Management

| Approach                       | Best for                     | Strengths                                  |
| ------------------------------ | ---------------------------- | ------------------------------------------ |
| **Component state**            | 単純なローカル操作           | 小さく、分かりやすく、影響範囲が狭い       |
| **Custom hooks / composables** | 再利用可能なローカルロジック | 振る舞いをカプセル化し、テストしやすくする |
| **Context / Provide-Inject**   | Subtree内で共有する状態      | 早すぎるGlobal state化を避けられる         |

### Recommendation

- 状態は**可能な限りローカルに保つ**。
- 繰り返し使われるロジックは**Hooks / Composables**へ抽出する。
- Global storeへ昇格させる前に、Subtree内での共有を検討する。

## Global State Management

| Style               | Best for                             | Trade-off                                  |
| ------------------- | ------------------------------------ | ------------------------------------------ |
| **Single store**    | 共有状態が単純な小規模アプリ         | 確認しやすいが、状態が増えると混雑しやすい |
| **Multiple stores** | 境界が明確な中規模から大規模のアプリ | 分離しやすいが、Store間の連携が多少増える  |

### Recommendation

- チーム規模だけを理由にGlobal stateを選ばない。
- **共有範囲**、**更新頻度**、**依存関係の複雑さ**を基準に選ぶ。
- Framework標準の仕組みだけでは不足する場合は、**Zustand**、**Pinia**、**Jotai**などの軽量なToolを優先する。

## Server State Management

| Approach                           | Best for                                                            | Notes              |
| ---------------------------------- | ------------------------------------------------------------------- | ------------------ |
| **Dedicated server-state library** | Cache、再取得、Loading/Error state、Optimistic updateが必要なアプリ | 推奨するデフォルト |
| **Generic store + API client**     | すでに別のStoreを中心に構成された小規模または特殊なケース           | 独自実装が増える   |

### Recommendation

次のような専用Libraryを使用する。

- **TanStack Query**
- **React Query / Vue Query**
- **SWR**

これらのLibraryによって、次の処理を簡単にできる。

- LoadingとError state
- Background refresh
- CacheとInvalidation
- Optimistic update
- Server側の正しい状態との同期

## Selection Heuristics

State管理Toolを選ぶ際は、次の観点で評価する。

- アプリ内で支配的なStateは何か
- どの程度の頻度で変化するか
- どの範囲で共有されるか
- State間の依存関係はどの程度複雑か
- 非同期取得やCache動作がどの程度必要か
- 機密データが含まれるか
- まずFramework標準の仕組みで解決できないか

## Recommended Evolution Path

1. **Framework defaults**から始める。
2. 再利用可能なローカルロジックには**Custom hooks / Composables**を追加する。
3. APIの複雑さが増えたら、**Server-state tooling**を導入する。
4. 本当に共有が必要なClient stateが現れた場合のみ、**軽量なGlobal state**を追加する。

## State Anti-Patterns

| Anti-pattern                          | Problem                                                       | Better choice                                   |
| ------------------------------------- | ------------------------------------------------------------- | ----------------------------------------------- |
| **Making everything global**          | 所有者が曖昧になり、Debugが難しくなり、不要な再Renderが増える | 共有が必要でない限りStateをローカルに保つ       |
| **Adding a heavy store too early**    | 価値がない段階で学習コストとBoilerplateが増える               | 単純な構成から始め、段階的に拡張する            |
| **Mixing app state and server state** | 責務が崩れ、同期処理が複雑になる                              | 別々に管理する                                  |
| **Unclear tool combinations**         | チーム内で一貫性がなくなる                                    | どの種類のStateをどのToolが管理するか文書化する |

## URL and Browser Storage Integration

| Storage target       | Good for                                        | Notes                         |
| -------------------- | ----------------------------------------------- | ----------------------------- |
| **URL query params** | 共有可能なFilterや検索条件                      | Deep linkに最適               |
| **localStorage**     | User設定、Draft、Browser終了後も保持したいState | 同一OriginのTab間で共有される |
| **sessionStorage**   | Tab単位の一時的なState                          | Tabを閉じると削除される       |
| **In-memory cache**  | 高速な一時値                                    | Refreshすると失われる         |

### Rule

Storageへのアクセスは、Hooks、Store、Moduleの背後に隠蔽する。UI Component全体へ生の `localStorage` アクセスを分散させない。

## Cache Strategy

### Browser Cache

次のようなStatic assetにはHTTP Cacheを使用する。

- CSS
- JavaScript bundle
- Image

代表的な制御方法には、次のものがある。

- `Cache-Control`
- `ETag`
- `Last-Modified`
- Asset versioning / Cache busting

### Application Cache

Application levelのCacheは、次のようなデータに対して慎重に使用する。

- Master data
- Settings
- 短時間の不整合を許容できるデータ

### Cache Recommendations

- **Static file**は積極的にCacheする。
- 許容できる場合は、ThemeやSettingsのような値をアプリ内でCacheする。
- API Responseは、デフォルトではCacheしない。
- API DataをCacheする場合は、有効期限、Invalidation、Logout時の削除を明確に定義する。
- 強い理由と保護戦略がない限り、機密データを保存しない。

## Offline / PWA Guidance

Offline対応はArchitectureを変えるため、安易に追加しない。

### Key Warnings

- PWAはNative mobile appを完全には置き換えない。
- Offline対応では、DataやLogicが重複することが多い。
- Service workerは1画面だけではなく、Frontend全体へ影響する。

### Static Asset Cache Strategy

| Strategy                                                      | Recommended use                 |
| ------------------------------------------------------------- | ------------------------------- |
| **Network-first**                                             | 通常のWeb Appにおけるデフォルト |
| **Cache-first / Stale-while-revalidate / Cache-then-network** | Static contentが中心の公開Site  |
| **Cache-only**                                                | 通常のOffline Web Appでは避ける |
| **Network-only**                                              | Offline利用では避ける           |

### Offline Storage

本格的なOffline機能には、`localStorage` より**IndexedDB**を優先する。

- 構造化された大容量データを扱える
- 非同期で動作する
- Service workerからアクセスできる

### Offline Logic Placement

- 新しいWeb Appでは、Offline用のBusiness logicをまず**Client-side application code**へ実装する。
- Service workerは慎重に扱い、主にCacheやProxy動作へ使用する。
- 可能な限りFramework ecosystemのToolを利用する。
  - `vite-pwa`
  - `next-pwa`
  - `workbox`

### Offline Detection

- `navigator.onLine` を主要な判断基準として使用しない。
- 実際のRequestとNetwork error handlingによってOffline状態を検出する。
- Userに明示的なMode切り替えを強制せず、Offline時の動作へ自動的に切り替える。
