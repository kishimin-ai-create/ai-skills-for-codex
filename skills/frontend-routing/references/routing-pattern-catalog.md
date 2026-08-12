# Routing Pattern Catalog

## Route categories

| Category      | Typical policy                                             |
| ------------- | ---------------------------------------------------------- |
| Public        | SEO metadata、キャッシュ、共有URL、匿名アクセスを検証      |
| Authenticated | サーバー側セッション検証、期限切れ遷移、noindex            |
| Authorized    | 権限ポリシーをサーバーで検証し、拒否と未認証を分ける       |
| API           | 入力・認証・エラー・CORS・タイムアウト・キャッシュを契約化 |
| Error         | 404、403、401、500、再試行、ログ相関を定義                 |

## Navigation

- 同一ドキュメント内のリンクはフレームワークのLinkを使い、外部リンクは明示する。
- 戻る・進む、直接URL、再読み込み、別タブ、共有URLを同じ契約として検証する。
- フィルターやページ番号など再現可能な状態はクエリへ置き、秘密・一時状態は置かない。
- モーダルやドロワーをURLで表す場合は、履歴追加・置換・閉じる操作を定義する。
- 遷移後にページタイトル、主見出し、フォーカスを更新する。

## Redirect safety

- ログイン後のreturn URLは相対パスまたは許可済みOriginだけを受け付ける。
- 正規化ルールを一箇所に集約し、末尾スラッシュ、大文字小文字、旧URL移行を一貫させる。
- ルートガードが自分自身へ遷移する条件を持たないことを確認する。

## Data and errors

- パラメータの型・範囲・存在を検証してからデータ取得する。
- loading、empty、not found、forbidden、unauthorized、errorを別状態として扱う。
- ルート変更時に古いリクエストをAbortし、遅れて返った結果で新しい画面を上書きしない。
- 404や権限不足で機密情報や内部エラーを表示しない。

## SEO and delivery

- 公開ページはtitle、description、canonical、OGP、sitemap、構造化データを確認する。
- 認証ページ、検索結果、一時URLは適切にnoindexまたはrobotsで制御する。
- SSR、SSG、CSR、再検証はSEO、データ鮮度、運用コスト、失敗時表示で選ぶ。
