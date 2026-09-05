---
name: frontend-folder-structure
description: bulletproof-reactを土台にしたReact/TypeScriptフロントエンドのディレクトリ構成（src/api, app/{providers,routes,schemas,tests,views}, components, features/<feature>/{schemas,tests,types,views}, gen, hooks, images, lib, models, providers, schemas, tests, theme, types, utils）で、新規ファイルの置き場所を判断し、新規プロジェクトの雛形を作成し、既存コードや設計ドキュメントの配置をレビューするときに使用する。「フォルダ構成」「ディレクトリ構造」「どこに置く」「新しい機能を追加」「Zodスキーマはどこに置く」「この型はどこ」「フロントエンドの雛形を作って」といった発話でも、bulletproof-reactへの明示的な言及がなくても積極的に使用する。
---

# Frontend Folder Structure

React/TypeScriptフロントエンドのディレクトリ構成を、bulletproof-reactを土台にした独自規約で設計・適用・レビューする。新規プロジェクトの雛形作成、新しいファイルの配置判断、既存コードや設計ドキュメントの配置レビューで使用する。

## 全体構成

```text
src/
├── api/            # バックエンドと通信する共有APIクライアント本体（fetch/axiosインスタンス等）
├── app/            # ルーティングとアプリ全体の組み立て。featureに依存しない
│   ├── providers/  # このアプリで使うProviderの合成（どのProviderをどの順で適用するか）
│   ├── routes/     # ルート定義
│   ├── schemas/    # app全体・ルーティングに関わるスキーマ（env、レイアウト等）
│   ├── tests/      # ルーティング・アプリ全体の結合テスト
│   └── views/      # 1つ以上のfeatureを組み合わせたページ単位のView
├── components/     # feature非依存の共有UIコンポーネント
├── features/
│   └── <feature>/
│       ├── schemas/  # このfeatureに閉じたバリデーションスキーマ
│       ├── tests/    # このfeatureに閉じたテスト
│       ├── types/    # このfeatureに閉じたUI専用の型
│       └── views/    # このfeatureのUI本体
│           # api/hooks/stores等は実際に必要になった時だけ追加する（YAGNI）
├── gen/            # OpenAPI等からの自動生成コード。手動編集禁止
├── hooks/          # 複数featureで再利用する共有Hooks
├── images/         # importして使う画像アセット
├── lib/            # サードパーティライブラリの薄いラッパー・設定
├── models/         # gen/の生成物を土台にした、手書きのAPIドメイン型・変換関数
├── providers/      # 個々の再利用可能なProvider実装
├── schemas/        # 複数featureで再利用する共有バリデーションスキーマ
├── tests/          # 共有テストインフラ（モック、setup、カスタムrender）
├── theme/          # デザイントークン・Tailwindテーマ設定
├── types/          # 複数featureで再利用するUI専用の型（APIドメイン型は含まない）
└── utils/          # サードパーティに依存しない共有純粋関数
```

`public/`直下（アイコン等）はimportせずそのまま配信する未加工の静的ファイル専用とし、importして使う画像は`src/images/`に置く。

## 配置決定ワークフロー

新しいファイルを追加するときは、次の順で置き場所を決める。迷ったときの詳しい判断例は[folder-responsibilities.md](./references/folder-responsibilities.md)を参照する。

### 1. 自動生成コードか

OpenAPIなどのスキーマから生成された型・クライアントコードは`gen/`に置き、手動編集しない。再生成コマンドで更新する前提を崩さないよう、`gen/`配下からアプリケーションコードをimportしない。

### 2. schemas / tests / providers はスコープで3段階に分ける

この3種類は「誰が使うか」でsrc直下・app/配下・features/<feature>配下のどこに置くかが変わる。

| スコープ | 置き場所 | 判断基準 |
| --- | --- | --- |
| 機能に閉じる | `features/<feature>/{schemas,tests,providers}` | そのfeatureだけが使う |
| app全体・feature非依存 | `app/{schemas,tests,providers}` | ルーティング・レイアウトなどfeatureに依存しないがアプリ全体に関わる |
| 複数featureで共有 | `{schemas,tests,providers}`（src直下） | 2つ以上のfeatureで再利用する、または汎用的（例: emailバリデータ、テスト用カスタムrender、ThemeProvider本体） |

判断は「その機能だけが使うか」から始め、Noなら「featureをまたいで使うか」で残り2つを分ける。

### 3. 型はAPIドメインかUI専用かで分ける

- APIレスポンスに対応するドメインの型、`gen/`生成物を土台にした変換関数 → `models/`
- 送信中/成功/エラーのUnion型のような、APIの形と直接対応しないUI専用の型 →
  - 1つのfeatureだけで使う → `features/<feature>/types/`
  - 複数featureで再利用する → `types/`（src直下）

`models/`と`types/`のどちらか迷ったら、「バックエンドのレスポンス形が変わったら追従して直す必要があるか」で判断する。Yesなら`models/`。

### 4. コンポーネントは責務の広さで分ける

- 特定のfeatureに依存しない汎用UI（Button、Inputなど） → `components/`
- 1つ以上のfeatureを組み合わせたページ → `app/views/`
- featureそのものの画面・フォーム → `features/<feature>/views/`

### 5. その他の共有リソース

- 複数featureで使うカスタムHooks → `hooks/`
- サードパーティライブラリの設定・ラッパー（queryClientインスタンス、`cn()`など） → `lib/`
- ライブラリに依存しない純粋なユーティリティ関数 → `utils/`
- デザイントークン・Tailwindテーマ拡張 → `theme/`
- バックエンドと通信する共有APIクライアント本体（エンドポイント別の呼び出しではなくクライアント設定） → `api/`

## 新規プロジェクトの雛形を作る場合

新規プロジェクトの立ち上げやディレクトリの一括作成を依頼された場合は、上記の`全体構成`をそのまま`src/`配下に作成する。ただし`features/<feature>/`は空のfeatureフォルダを量産せず、実際に依頼された機能名でのみ作成し、`schemas/tests/types/views`もそのfeatureで実際に必要なものだけを作る。

## 既存コードのレビュー時

コンポーネント設計ドキュメントやPull Requestの配置が、上記の判断基準（特にschemas/tests/providersの3段階スコープと、models/types/gen/の使い分け）に沿っているかを確認する。逸脱している場合は、意図的な例外か判断ミスかを確認してから指摘する。

## 出力契約

フォルダ構成の提案・作成・レビュー結果と併せて、次を報告する。

1. 対象のファイル・機能と、それをどこに置いたか（置くべきか）
2. 判断根拠（配置決定ワークフローのどの基準を使ったか）
3. 新規に作成したディレクトリ・ファイルの一覧（雛形作成の場合）
4. 規約から意図的に外れた点があれば、その理由
