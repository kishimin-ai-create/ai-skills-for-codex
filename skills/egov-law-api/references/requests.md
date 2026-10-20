# 呼び出し例と取得上の注意

2026-10-20に公式OpenAPI（`info.version: 2.1.139`）と実APIを確認した。仕様の正本は [lawapi-v2.yaml](https://laws.e-gov.go.jp/api/2/swagger-ui/lawapi-v2.yaml)。以下は読み取り用の例で、法令・対象日・取得件数を依頼に合わせて変更する。

## HTTPクライアント

利用できる既存のクライアントを使う。以下の例は `curl`。Windows PowerShellでは別名との衝突を避けて `curl.exe` を使用する。`--get --data-urlencode` により、日本語、`+`、角括弧、検索式をクエリ値としてエンコードする。

### 法令名の検索

```sh
curl --fail-with-body --silent --show-error --max-time 30 --get 'https://laws.e-gov.go.jp/api/2/laws' --data-urlencode 'law_title=デジタル庁設置法' --data-urlencode 'limit=3' --data-urlencode 'response_format=json'
```

結果は `laws[]`。IDと番号は `law_info`、法令名と履歴IDは `revision_info` にある。`law_title` は部分一致。`count` と全件数の `total_count` を区別する。必要な場合だけ `next_offset` で続きを取得する。

### キーワード検索

```sh
curl --fail-with-body --silent --show-error --max-time 30 --get 'https://laws.e-gov.go.jp/api/2/keyword' --data-urlencode 'keyword=デジタル庁' --data-urlencode 'limit=2' --data-urlencode 'response_format=json'
```

結果は `items[]`。`sentences[].position` は本文取得の `elm` に使える。`sentences[].text` はハイライトタグを含む抜粋で、全文ではない。本文APIで原文を再取得する。

`limit` は法令数ではなく `sentences` の `position` 数の総和の上限で、仕様上の上限は1000。`sentence_count` と法令数を混同しない。`sentences_limit` を指定すると要求件数と取得件数が一致しない場合がある。検索式のAND・OR・NOTは[公式の検索式](https://laws.e-gov.go.jp/help/#how-to-write-a-search-expression)を確認し、ワイルドカードとの併用はしない。

### 改正履歴

```sh
curl --fail-with-body --silent --show-error --max-time 30 --get 'https://laws.e-gov.go.jp/api/2/law_revisions/503AC0000000036' --data-urlencode 'response_format=json'
```

結果は `law_info` と `revisions[]`。`law_revision_id`、`amendment_enforcement_date`、`current_revision_status` を確認する。履歴APIに `asof` や `limit` を流用しない。施行期日で絞る場合は `amendment_date_from` / `amendment_date_to` を使用する。

### 第1条の本文

```sh
curl --fail-with-body --silent --show-error --max-time 30 --get 'https://laws.e-gov.go.jp/api/2/law_data/503AC0000000036' --data-urlencode 'elm=MainProvision-Article_1' --data-urlencode 'response_format=json' --data-urlencode 'law_full_text_format=json'
```

結果の `law_full_text` は標準の `json_format=full` では `tag`、`attr`、`children` による木構造。`children` は文字列と要素を含むため、文章だけでなく項・号・見出しの境界も保って読む。簡易版を使う場合は `json_format=light` と[簡易版スキーマ](https://laws.e-gov.go.jp/api/2/swagger-ui/lawapi-v2-json-light-schema.yaml)を確認する。

`elm` は汎用XPathではない。例えば `MainProvision-Article_1-Paragraph_2`。条番号の枝番や附則などは実際の構造と公式の `elm` 定義を確認し、取得結果の条・項番号も照合する。`Article_1` と位置指定の `[1]` を取り違えない。`elm` を省略すると全文になる。

過去時点には同じリクエストへ `asof=2024-04-01` を追加できる。版の再現が必要なら、取得した `law_revision_id` を本文パスに使用する。本文・レスポンス形式を異ならせた場合は、文字列の `law_full_text` をBase64デコードしてから指定形式として扱う。

## 本文ファイルと添付

本文ファイルは `/law_file/xml/{law_id_or_num_or_revision_id}` などで取得する。対応形式は `xml`, `json`, `html`, `rtf`, `docx`。PDFを `file_type` として作らない。レスポンスはファイル本体であり、本文APIのJSONエンベロープとして扱わない。

添付は本文と同じ `law_revision_id` と、その本文の `Fig` 要素にある `src` を使用する。`src` の例は `./pict/H11HO127-001.jpg`。この相対パスをAPIのパスへ連結せず、`/attachment/{law_revision_id}` の `src` クエリ値としてエンコードする。

ファイルは依頼された保存先または作業用ディレクトリへ保存する。HTTPステータスとContent-Typeを確認し、エラーJSONを成功したファイルとして報告しない。既存ファイルの上書きを避け、保存先と取得した版を報告する。大量の法令が必要なら[公式XML一括ダウンロード](https://laws.e-gov.go.jp/bulkdownload/)も検討する。

## 実測とエラー

- 上記4例はHTTP 200と対応する構造を確認済み。履歴の件数や最新の履歴IDは固定値として扱わない。
- 本文ファイル・添付の取得先は公式仕様で確認済み。取得するファイルごとのステータスと内容は実行時に検証する。
- 公式エラー形式は `code` と `message`。非JSONの障害ページの場合もあるため、HTTPステータスとContent-Typeを見てからパースする。
- 空の検索結果と通信失敗を区別する。取得が途中で止まった場合は、取得範囲と次のoffsetを残し、全件取得済みとは報告しない。
- `repeal_status` が `Expire` / `LossOfEffectiveness` の `repeal_date` はデータ廃止処理日で、実際の廃止日とは限らない。
