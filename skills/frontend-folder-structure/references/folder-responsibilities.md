# フォルダ責務リファレンス

各フォルダの責務、含めてよい例、含めてはいけない例（代わりにどこへ置くか）をまとめる。[SKILL.md](../SKILL.md)の配置決定ワークフローで判断に迷ったときに参照する。

## src/api/

- 責務: バックエンドと通信する共有APIクライアント本体（fetch/axiosインスタンス、ベースURL・ヘッダー・インターセプターの設定）
- 含めてよい例: `apiClient.ts`（インスタンス生成）、共通のエラーレスポンス変換
- 含めてはいけない例: 個別エンドポイントの呼び出し関数（feature側の`views/`や、必要になったら追加する`features/<feature>/api/`に置く）

## src/app/providers/

- 責務: このアプリで使うProviderの合成。どのProviderをどの順で適用するかのワイヤリング
- 含めてよい例: `AppProviders.tsx`（QueryClientProvider・ThemeProvider・i18nProviderをまとめてラップする）
- 含めてはいけない例: Provider自体の実装（`src/providers/`に置き、ここではimportして組み立てるだけにする）

## src/app/routes/

- 責務: ルート定義（パスとViewの対応）
- 含めてよい例: ルーター設定、ルートツリー
- 含めてはいけない例: ルートに表示するページの中身（`src/app/views/`に置く）

## src/app/schemas/

- 責務: featureに依存しない、app全体・ルーティングに関わるスキーマ
- 含めてよい例: 環境変数のバリデーションスキーマ、レイアウト共通のクエリパラメータスキーマ
- 含めてはいけない例: 特定featureのフォーム入力スキーマ（`features/<feature>/schemas/`）、複数featureで再利用する汎用スキーマ（`src/schemas/`）

## src/app/tests/

- 責務: ルーティング・アプリ全体にまたがる結合テスト
- 含めてよい例: 「未知のパスにアクセスすると404ページが表示される」といったapp全体のテスト
- 含めてはいけない例: 1つのfeatureに閉じたテスト（`features/<feature>/tests/`）

## src/app/views/

- 責務: 1つ以上のfeatureを組み合わせたページ単位のView
- 含めてよい例: `HomePage.tsx`（複数featureのViewを合成する）、`NotFoundPage.tsx`
- 含めてはいけない例: featureそのものの画面・フォーム（`features/<feature>/views/`）

## src/components/

- 責務: feature非依存の共有UIコンポーネント（表示とアクセシビリティのみ）
- 含めてよい例: `Button`、`TextField`、`Select`などのプリミティブとその合成
- 含めてはいけない例: グローバル状態・ルーティング・データ取得への直接依存。特定featureにしか使わないコンポーネント（`features/<feature>/views/`）

## src/features/\<feature\>/schemas/

- 責務: そのfeatureに閉じたバリデーションスキーマ
- 含めてよい例: そのfeature固有のフォーム入力スキーマ
- 含めてはいけない例: 2つ以上のfeatureで再利用するスキーマ（`src/schemas/`へ昇格する）

## src/features/\<feature\>/tests/

- 責務: そのfeatureに閉じたテスト
- 含めてよい例: そのfeatureのコンポーネント・Hookのテスト
- 含めてはいけない例: 複数featureにまたがるテスト、app全体のテスト（`src/app/tests/`）

## src/features/\<feature\>/types/

- 責務: そのfeatureに閉じたUI専用の型（APIの形と直接対応しない型）
- 含めてよい例: そのfeature内の送信状態を表すDiscriminated Union
- 含めてはいけない例: APIレスポンスに対応するドメイン型（`src/models/`）、複数featureで再利用するUI型（`src/types/`）

## src/features/\<feature\>/views/

- 責務: そのfeatureのUI本体
- 含めてよい例: フォーム、一覧画面、そのfeature固有の画面コンポーネント
- 含めてはいけない例: 他featureからも使う汎用コンポーネント（`src/components/`へ昇格する）

`features/<feature>/`配下の`api/`、`hooks/`、`stores/`などは、実際にそのfeatureで必要になるまで作らない。空のフォルダを雛形として量産しない。

## src/gen/

- 責務: OpenAPI等のスキーマから自動生成されたコード（型・APIクライアント）の出力先
- 含めてよい例: codegenツールの出力そのもの
- 含めてはいけない例: 手動編集（次回の再生成で上書きされる）。`gen/`からアプリケーションコードをimportすること（依存の向きは`gen/` → `models/` → featureの一方向を保つ）

## src/hooks/

- 責務: 複数featureで再利用する共有カスタムHooks
- 含めてよい例: `useDebounce`、`useMediaQuery`など汎用的なHooks
- 含めてはいけない例: 1つのfeatureでしか使わないHooks（そのfeature配下に置く。必要になったら`features/<feature>/hooks/`を作る）

## src/images/

- 責務: importして使う画像アセット（バンドラーが処理する）
- 含めてよい例: `import logo from "@/images/logo.svg"`のように参照する画像
- 含めてはいけない例: importせず直接配信するファイル（`public/`直下）

## src/lib/

- 責務: サードパーティライブラリの薄いラッパー・初期化設定
- 含めてよい例: `queryClient`インスタンス、`cn()`（clsx + tailwind-merge）、日付ライブラリの初期設定
- 含めてはいけない例: 自作の汎用ロジックでライブラリに依存しないもの（`src/utils/`）

## src/models/

- 責務: `gen/`の生成物を土台にした、手書きのAPIドメイン型・変換関数（アダプター）
- 含めてよい例: `gen/`が生成した生のレスポンス型を、アプリで扱いやすいドメイン形へ変換する関数と、その結果の型
- 含めてはいけない例: バックエンドのレスポンス形と無関係なUI専用の型（`src/types/`または`features/<feature>/types/`）

## src/providers/

- 責務: 個々の再利用可能なProvider実装
- 含めてよい例: `ThemeProvider`、`I18nProvider`など、それ単体で完結したProviderコンポーネント
- 含めてはいけない例: どのProviderをどの順で組み合わせるかのワイヤリング（`src/app/providers/`）

## src/schemas/

- 責務: 複数featureで再利用する共有バリデーションスキーマ
- 含めてよい例: emailバリデータ、ページネーションパラメータのスキーマなど汎用的なもの
- 含めてはいけない例: 1つのfeatureでしか使わないスキーマ（`features/<feature>/schemas/`）

## src/tests/

- 責務: 共有テストインフラ（モックサーバー、setupファイル、カスタムrender関数）
- 含めてよい例: `render`のラッパー、MSWのハンドラー共通部分
- 含めてはいけない例: 実際のテストケース（それぞれのスコープ＝`app/tests/`・`features/<feature>/tests/`に置く）

## src/theme/

- 責務: デザイントークン・Tailwindテーマ拡張などスタイルの一元設定
- 含めてよい例: カラーパレット、spacingスケール、Tailwind設定に渡すトークン定義
- 含めてはいけない例: 個々のコンポーネントのスタイル実装（各コンポーネント側）

## src/types/

- 責務: 複数featureで再利用するUI専用の型（APIドメイン型は含まない）
- 含めてよい例: `Nullable<T>`などの汎用ユーティリティ型、複数featureで共通のUI状態のUnion型
- 含めてはいけない例: APIレスポンスに対応する型（`src/models/`）、1つのfeatureでしか使わない型（`features/<feature>/types/`）

## src/utils/

- 責務: サードパーティに依存しない共有純粋関数
- 含めてよい例: フォーマッター、文字列・配列操作のヘルパー
- 含めてはいけない例: サードパーティライブラリのラップ・設定（`src/lib/`）
