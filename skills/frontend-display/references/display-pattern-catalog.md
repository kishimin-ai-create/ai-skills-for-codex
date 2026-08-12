---
name: frontend-display
description: "ブラウザ対応、レスポンシブレイアウト、ローカライズ、画像、ダークモード、配信パフォーマンスに関する指針。"
---

# Frontend Display

ブラウザ対応、レスポンシブルール、画像の扱い、ダークモード、i18n、フロントエンド配信パフォーマンスを定義する際に、このスキルを使用する。

## Browser Support Policy

### Core Browser Set

次のブラウザを、モダンブラウザ対応の標準的な基準として扱う。

- Google Chrome（デスクトップ / Android）
- Apple Safari（macOS / iOS）
- Microsoft Edge（デスクトップ）
- Mozilla Firefox（デスクトップ / Android）

### Recommendations

- 対応ブラウザの一覧は、実用上可能な限り**小さく保つ**。
- セキュリティアップデートが提供されているブラウザとOSバージョンを優先する。
- Chromeは、ほぼ常に対応対象へ含める。
- iOSでは、Safariを対応対象へ含める必要がある。
- ビジネス要件が許す場合は、利用率の低いブラウザを対応対象から外すことを検討する。

### Version Policy

- 自動更新されるデスクトップブラウザでは、**最新バージョンと1つ前のバージョン**をサポートする。
- Firefox対応が必要な場合は、最新版またはESR系統を使用する。
- モバイルでは、まず**対応OSと端末群**を定義し、そこからブラウザ対応範囲を決める。

## Responsive Design

レスポンシブ対応には、通常、次の項目が含まれる。

- 読みやすさを保つためのレイアウト調整
- タッチ操作しやすいボタンやリンクの配置
- 端末に適したフォントサイズ
- レスポンシブ画像配信
- CSSおよびJavaScriptサイズの最適化

## Breakpoint Strategy

| Technique             | Best for                   | Recommendation                                 |
| --------------------- | -------------------------- | ---------------------------------------------- |
| **Media queries**     | ページ全体のレイアウト変更 | グローバルなブレークポイントに使用する         |
| **Container queries** | コンポーネント単位の適応   | ページレベルのレイアウトが安定した後に追加する |

### Practical Rules

- ページシェル、ナビゲーション、余白、全体レイアウトには**Media queries**を使用する。
- 柔軟なレイアウト内のカード、ウィジェット、コンポーネントには**Container queries**を使用する。
- ブレークポイントの数は少なく保つ。
- Container queriesを深くネストしない。

## Tailwind CSS Guidance

Tailwind CSSを使用する場合は、次の方針に従う。

- 要件上必要でない限り、`sm`、`md`、`lg` などの標準的なレスポンシブプレフィックスを優先する。
- 既存のプレフィックス定義を大きく変更しない。
- カスタムブレークポイントを追加する場合は、意味が分かる名前を付ける。
- プレフィックスなしのクラスを**モバイルのデフォルト**として使用する。

```html
<div class="text-center sm:text-left"></div>
```

## Mobile-First Policy

- 社内システムであっても、デフォルトでは**モバイルファーストCSS**を採用する。
- 情報量の多い業務画面では、まずモバイルで表示する情報を減らせないか検討する。
- 1つのレイアウトで複数端末へ十分に対応できない場合は、次の順序で検討する。
  1. 1つのページ内での条件付き非表示、または代替マークアップ
  2. モバイル専用ページ
  3. モバイル固有の操作が中心である場合は、専用モバイルアプリ

## Resolution and Viewport

### Resolution Rules

- 設計とQAのために、1つの**対象論理解像度**を事前に定義する。
- デスクトップの一般的な基準としては、**1280x720程度の論理解像度**を使用できる。
- 具体的なテスト対象を定めずに、「1366x768以上」のような曖昧な要件を書かない。
- モバイルでは、縦向き専用で問題ないかどうかを明示的に決定する。

### Browser Window and Zoom

- デフォルトでは、ブラウザを全画面で使用する前提とする。
- 100%ズームを設計上の基準とする。
- Viewportが対象基準より小さくなった場合は、コントロールを壊すのではなく、スクロールによって操作性を維持する。

### Viewport Meta Tag

標準的なレスポンシブViewportを使用する。

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
```

例外的な理由がない限り、ズーム範囲を固定しない。UXとアクセシビリティを損なうためである。

## Internationalization (i18n)

- 初回リリースが単一言語であっても、i18nの仕組みを導入する。
- UIテキストは早い段階で外部化する。後から対応するとコストが高くなる。
- 強い理由がない限り、デフォルト言語の判定にはブラウザ言語を使用する。

### Useful Libraries

- React: `react-intl`, `react-i18next`
- Vue: `vue-i18n`, `unplugin-vue-i18n`
- Angular: `@ngx-translate/core`

## Image Strategy

| Asset type                         | Recommended format                                    |
| ---------------------------------- | ----------------------------------------------------- |
| ブランド素材、アイコン、ロゴ       | **SVG**                                               |
| 写真、商品画像、複雑なバナー       | **AVIF** または **WebP**                              |
| 図、スクリーンショット、透過UI画像 | **AVIF** または **WebP**                              |
| アニメーション画像                 | 可能な限り避け、CSS、JavaScript、または動画を使用する |

### Image Best Practices

- モダン形式とフォールバックを配信するために `<picture>` を使用する。
- レスポンシブ画像には `srcset` と `sizes` を使用する。
- 配信前に元画像を最適化する。
- ファーストビュー外の画像には `loading="lazy"` を使用する。
- 情報を伝える画像には、意味のある `alt` テキストを設定する。
- 装飾目的の画像には `alt=""` を使用する。

## OGP and Favicon

### OGP

- OGPは主に、一般公開され、共有可能な一般ユーザー向けページで重要になる。
- 社内アプリや認証後のプライベートSaaSページでは、通常OGPは不要である。

```html
<meta property="og:title" content="Page title" />
<meta property="og:description" content="Page description" />
<meta property="og:image" content="https://example.com/og-image.png" />
<meta property="og:url" content="https://example.com/page" />
```

### Favicon Set

推奨する最小構成は次のとおり。

- `icon.svg`
- `apple-touch-icon.png`
- `icon-192.png`
- `icon-512.png`
- `manifest.webmanifest`
- `favicon.ico` はレガシーフォールバック用途のみ

**SVGを優先**し、プラットフォーム要件に応じてPNGファイルを補助的に用意する。

## Dark Mode

### Recommended Model

**Hybrid strategy**を使用する。

- ユーザーのOS設定をデフォルトにする
- 手動のテーマ切り替えも提供する
- ユーザーが明示的に選択した内容を保存する

### Persistence

- 端末間同期が不要な場合は、デフォルトで**localStorage**を使用する。
- ストレージを利用できない場合は、メモリ上の状態へフォールバックする。
- 複数のブラウザ、端末、ドメイン間で設定を引き継ぐ必要がある場合のみ、サーバー側へ保存する。

### Dark Mode QA

次の項目を明示的に確認する。

- テキストのコントラスト
- アイコンやイラストの視認性
- 透過画像の背景
- フォーカス状態
- 両方のテーマでの読みやすさ

## Delivery Performance

### Minify and Source Maps

- 本番用アセットはMinifyし、転送サイズを削減するとともに、開発時の不要な情報が見えにくい状態にする。
- 必要に応じて、ローカル環境や開発環境ではSource Mapを保持する。
- セキュリティおよび運用方針で明示的に許可されていない限り、本番環境でSource Mapを公開しない。
- エラー監視ツールがSource Mapを必要とする場合は、非公開形式で生成し、アップロード後に公開状態を解除する。

### Environment Guidance

| Environment | Minify | Source maps                                  |
| ----------- | ------ | -------------------------------------------- |
| Local       | No     | Yes                                          |
| Development | Yes    | Yes                                          |
| Staging     | Yes    | 一時的なデバッグで必要な場合を除き、通常はNo |
| Production  | Yes    | デフォルトでは公開しない                     |

## Accessibility Reminders

アクセシビリティは表示設計の一部であり、後付けで対応するものではない。

- 読みやすいフォントサイズを維持する。
- タッチターゲットを十分な大きさにする。
- ライトテーマとダークテーマの両方で色のコントラストを維持する。
- 強い理由がない限り、ズームを無効化しない。
- キーボード操作と支援技術の利用フローを含めて、レスポンシブレイアウトをテストする。
