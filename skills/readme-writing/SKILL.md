---
name: readme-writing
description: リポジトリの実ファイル（依存定義、スクリプト、ディレクトリ、ルーティング、CI）を根拠に、Tech Stackバッジ・Table of Contents・Environment表・Directory Structure・Getting Started・Usage・Available Commands・Troubleshooting・back to topリンクを備えた英語のREADME.mdを作成、更新、レビューするときに使用する。「READMEを書いて」「READMEを作って」「READMEを整えて」「READMEが古いので直して」といった依頼はもちろん、新規リポジトリの初期整備、公開前のドキュメント整備、既存READMEと実装の乖離修正、リポジトリの説明文書の追加を扱うときにも積極的に使用する。
---

# README Writing

読者が上から順に読むだけで「何のリポジトリか」「どう動かすか」「詰まったらどうするか」に到達できるREADMEを作る。README は宣伝文ではなく、リポジトリの実体を写した参照文書として書く。実ファイルで確認できない値は書かない。

## 責務境界

- `README.md` の作成、更新、レビューだけを行う。
- コード、設定、依存関係、CI、ドキュメント本体を変更しない。README の記述を成立させるために実装を変えない。
- バージョン、コマンド、パス、エンドポイントは、リポジトリ内の実ファイルで確認した値だけを書く。
- コミットしない。コミットが必要なら適用される Git 規則、または `commit-changes` に従う。
- 実行していない検証を「動作確認済み」と書かない。
- 呼び出し元 Agent により書き込みが禁止されている場合は、その境界を優先する。

## 出力言語

既定は英語。リポジトリの既存 README、docs、コミットメッセージが一貫して日本語である場合、またはユーザーが指定した場合はその言語に合わせる。見出し名は本スキルの規定どおり英語のまま保つ。Table of Contents のアンカーが見出し文字列から生成されるため、見出しを訳すとリンクが壊れる。

## 1. 根拠を集める

README を書く前に、次を読む。読めなかったものは記録し、その領域については書かない。

| 対象 | 何を取るか |
| ---- | ---------- |
| 依存定義（`package.json`, `requirements.txt`, `setup.py`, `*.csproj`, `go.mod`, `Cargo.toml`, `pyproject.toml`） | 言語、フレームワーク、主要ライブラリ、宣言バージョン |
| lockfile（`bun.lock`, `package-lock.json`, `uv.lock`, `Cargo.lock`） | 実際に解決されたバージョン |
| スクリプト定義（`scripts`, `Makefile`, `Taskfile`, `justfile`） | Available Commands に載せるコマンド |
| エントリポイント、ルーティング定義、OpenAPI スキーマ | API Endpoints、Usage のコード例 |
| ディレクトリ（生成物と依存物を除く） | Directory Structure |
| CI ワークフロー | 実際に回っている検証コマンド、対応OS、ランタイムバージョン |
| `Dockerfile`, `compose.yaml`, デプロイ設定 | コンテナ手順、公開ポート、ヘルスチェック |
| 既存 README、`docs/`、ADR | About the Project、設計上の制約 |
| `LICENSE` | ライセンス表記の有無 |
| Issue、CI の失敗履歴、`.env.example` | Troubleshooting の実例 |

バージョンは、lockfile で解決値を確認できればそれを書く。確認できなければ依存定義の宣言値を書き、範囲指定（`^4.12.23`）はそのままの表記で書く。実行環境を推測して具体値を捏造しない。

## 2. 載せるセクションを決める

固定の骨格は次のとおり。条件付きセクションは、該当する根拠が実在するときだけ入れる。空の節を残さない。

| セクション | 条件 |
| ---------- | ---- |
| タイトルと1行説明 | 常に |
| `## Tech Stack` | 常に |
| `## Table of Contents` | 常に |
| `## About the Project` | 常に |
| `## Environment` | 常に |
| `## Directory Structure` | 常に |
| `## Getting Started` | 常に |
| `## Usage` | 常に |
| `## API Endpoints` | HTTP API を公開している場合 |
| `## Available Commands` | 常に |
| `## Troubleshooting` | 実際に踏んだ、または再現手順が確認できる問題が1件以上ある場合 |
| `## License` | `LICENSE` が存在する、または配布方針が決まっている場合 |

必要ならこの骨格に追加してよい（`## Architecture`、`## Configuration`、`## Deployment` など）。追加したら Table of Contents にも反映する。逆に、骨格のセクションを削るのは根拠が存在しない場合に限る。

## 3. テンプレートを適用する

雛形は `assets/readme-template.md` にある。読み込んで、プレースホルダを実際の値で置き換える。骨格の要素は次の3つで、これがこの README 形式の識別点になっている。

1. 先頭の `<div id="top"></div>`
2. 各セクション末尾の `<p align="right">(<a href="#top">back to top</a>)</p>`
3. 番号付きの Table of Contents

back to top リンクは `## About the Project` 以降の全セクションに付ける。タイトル、`## Tech Stack`、`## Table of Contents` には付けない。読者がまだ上部にいるためで、ここに付けると意味のない往復になる。

## 4. セクションごとの規則

### タイトルと1行説明

リポジトリ名を `#` 見出しにし、直後に1文で「何をするものか」を書く。動詞で始め、実装の内部事情ではなく成果物を書く。

```markdown
# glyph-forge

Generate glyph art images by filling a text-shaped frame with repeated text.
```

### Tech Stack

shields.io のバッジを `for-the-badge` で並べる。順序は 言語 → フレームワーク → 主要ライブラリ → テスト・品質ツール。ロゴのスラッグと色を推測しない。よく使う技術の確定値は `references/badges.md` にある。載っていない技術は、ロゴを省いて `-000000` の無地バッジにする（誤ったスラッグは壊れた画像として表示されるため、無地の方が安全）。

バッジは4〜6個に絞る。開発依存を全部並べると、何が中心技術か読み取れなくなる。

### Table of Contents

番号付きリストで、実在する `##` 見出しだけを並べる。アンカーは見出しを小文字化し、空白をハイフンに、英数字とハイフン以外を除去して作る（`## Getting Started` → `#getting-started`）。`###` 見出しは含めない。

### About the Project

まず、このリポジトリの中心概念を箇条書きで定義する。ドメイン固有の名前（パラメータ名、エンティティ名、モード名）があるなら、ここで意味を与えるのが最も効く。読者はこの後の Usage をその語彙で読むことになる。

続けて1〜2段落で、何ができるか、どういう性質を持つかを書く。マーケティング文ではなく、機能の範囲を書く。

### Environment

`| Language / Framework | Version |` の2列表。実行に必要なものだけを載せ、リンタやフォーマッタは載せない（それらは Available Commands に出る）。表の下に、完全な依存一覧の在り処を1文で示す。

```markdown
See `requirements.txt` and `setup.py` for the full dependency and package metadata.
```

### Directory Structure

` ```text ` のツリーを書き、その後に `### Main Directories` 表で各ディレクトリの責務を1行ずつ説明する。

- 生成物と依存物を含めない（`node_modules`, `dist`, `.next`, `storybook-static`, `.venv`, `target`, `__pycache__`）。これらを載せると、実際の構成を読み取れなくなる。
- 深さは2〜3階層まで。葉のファイルを網羅しない。
- ルート直下の重要なファイル（`Dockerfile`, `LICENSE`, 設定ファイル）はツリーに含めてよいが、`### Main Directories` 表はディレクトリだけにする。
- 実際のディレクトリ名と一致させる。将来作る予定の構成を書かない。

### Getting Started

読者が上から順に実行すれば動く順序にする。各手順は見出し（`###`）＋短い説明＋コードブロック。

1. `### Prerequisites` — 必要なランタイムとそのバージョン
2. `### Clone the Repository`
3. 環境準備（仮想環境、`.env` の作成など。不要な言語では省く）
4. 依存インストール
5. テスト実行
6. アプリケーション起動と、開くURL
7. コンテナ実行（`Dockerfile` がある場合）

OS でコマンドが変わる箇所は、両方を別のコードブロックで示す。片方だけ書くともう片方の読者が止まる。

````markdown
On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
````

コードブロックには必ず言語を指定する（`bash`, `powershell`, `text`, `json` など）。URL やパスだけのブロックは `text` にする。

### Usage

最小の動作例を1〜2個載せる。抜粋ではなく、そのままコピーして動くものにする。

API へのリクエスト例では、`curl` の長い引用符やヒアドキュメントを避け、その言語の標準ライブラリで書く。シェルによってクォートの解釈が変わり、読者の環境で失敗するため。glyph-forge の README がこれを明示しているのは、実際にそこで詰まるからである。

### API Endpoints

HTTP API がある場合のみ。

1. `| Method | Path | Description |` の一覧表
2. `### Request Body` — `| Field | Required | Default | Description |` の表
3. 表で表せない制約を散文で書く

散文で書くのは、フィールド単体では表現できない条件である。相互排他（「両方を空白のみにはできない」）、上限（画像サイズ、アップロードサイズ、総ピクセル数）、レート制限とキューの挙動、タイムアウト、返るステータスコード。**上限値と、上限超過時に返るステータスコードは必ず書く**。これを書かない README は、読者が本番で 4xx を踏んでから調べ直すことになる。

### Available Commands

`| Command | Description |` の表。`scripts` や `Makefile` に実在するものだけを、開発者が実際に打つ順（インストール → テスト → 静的解析 → 起動 → ビルド）で並べる。存在しないコマンドを「あるべき姿」として載せない。

### Troubleshooting

`### ` の見出しに**実際のエラーメッセージか症状をそのまま**書き、原因を1〜2文、対処をコードブロックで示す。読者はエラー文字列で検索するため、見出しが実物と一致していることに価値がある。

````markdown
### `ModuleNotFoundError: glyph_forge`

Install the package in editable mode.

```bash
pip install -e .
```
````

想像上のエラーを書かない。採取元は、CI の失敗履歴、Issue、`.env.example` の必須項目漏れ、セットアップ中に自分が実際に踏んだ失敗である。1件も見つからないなら、このセクションを省く方が正しい。

## 5. 自己検証

書き終えたら、次を実ファイルと突き合わせる。README は嘘をつくと発見が遅く、読者は先に信用を失う。

- [ ] Table of Contents の全リンクが、実在する `##` 見出しに解決する
- [ ] `## About the Project` 以降の全セクション末尾に back to top リンクがある
- [ ] Environment 表のバージョンが依存定義または lockfile と一致する
- [ ] Available Commands の全コマンドがスクリプト定義に実在する
- [ ] Directory Structure のディレクトリが実在し、生成物を含まない
- [ ] API Endpoints のパスとフィールドがルーティング定義またはスキーマと一致する
- [ ] 全コードブロックに言語指定がある
- [ ] 未実装の機能、将来の予定を現在形で書いていない
- [ ] シークレット、トークン、個人のメールアドレス、内部URLを含まない
- [ ] リポジトリの Prettier / markdownlint 設定がある場合、その整形規則に従っている

コマンドを実際に実行して検証した場合は、その事実と結果を報告に含める。実行していないなら、記載は「実ファイルとの一致を確認した」までに留める。

## 完了条件

- `README.md` が作成または更新され、骨格のセクションが揃っている。
- 記載された全バージョン、コマンド、パス、エンドポイントの根拠ファイルを示せる。
- 根拠が無いために省いたセクションと、その理由を報告している。
- 実行した検証と、未実行の検証を区別して報告している。
