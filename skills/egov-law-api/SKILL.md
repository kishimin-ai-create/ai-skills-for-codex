---
name: egov-law-api
description: e-Gov法令API Version 2を呼び出し、日本の法令名・本文の検索、条文取得、改正履歴の確認、法令ファイル・添付ファイルの取得を行う。e-Gov APIによる法令データの調査や取得を依頼されたときに使用する。
---

# e-Gov Law API

e-Govの一次データを取得し、取得した版と時点を明示して回答する。

## 仕様と呼び出し先

- APIベースURL: `https://laws.e-gov.go.jp/api/2`
- [Swagger UI](https://laws.e-gov.go.jp/api/2/swagger-ui)
- [OpenAPI仕様](https://laws.e-gov.go.jp/api/2/swagger-ui/lawapi-v2.yaml)
- [法令データの構造](https://laws.e-gov.go.jp/docs/)

Swagger UIは仕様の閲覧先。データ取得にはAPIベースURL配下のGETを使う。2026-10-20確認の仕様は `info.version: 2.1.139` で、認証の指定はない。APIキーを独自に要求しない。パラメータ・列挙値・レスポンス構造が不明な場合は公式OpenAPIを再確認する。

## 進め方

1. 依頼から法令名、キーワード、条項、対象日、必要な形式を読み取る。対象日が指定されていなければ現在のデータを取得し、取得日を示す。結果を変える曖昧さだけ確認する。
2. 下表からAPIを選ぶ。法令名だけが分かる場合は `/laws` で候補と `law_id` を確認してから本文・履歴を取得する。複数候補があれば完全な法令名と番号で識別し、同名・略称を推測で確定しない。
3. [呼び出し例と取得上の注意](references/requests.md)を読み、利用可能なHTTPクライアントで実行する。日本語や検索式はクエリとしてURLエンコードし、パスの識別子も1セグメントとしてエンコードする。
4. HTTPステータスとレスポンスの構造を確認する。キーワード検索の抜粋は本文APIで再取得し、条文の根拠にする。必要な範囲だけ取得し、全文・バイナリを不用意に会話へ展開しない。
5. 法令名、法令番号、`law_id`、`law_revision_id`、指定した時点、取得日、参照URLを添えて結果を示す。原文引用と要約を区別し、取得できなかった範囲は明記する。

## APIの選択

以下はすべてGET。詳細なフィルターと値の定義は公式OpenAPIを確認する。

| 目的 | パス | 主な指定 |
| --- | --- | --- |
| 法令名・略称・番号から探す | `/laws` | `law_title`, `law_num`, `law_id`, `asof`, `limit`, `offset` |
| 本文をキーワード検索する | `/keyword` | 必須の `keyword`, `asof`, `limit`, `offset` |
| 改正履歴と施行状態を調べる | `/law_revisions/{law_id_or_num}` | 法令IDまたは法令番号、必要に応じて施行期日の範囲 |
| 全文・特定条項を取得する | `/law_data/{law_id_or_num_or_revision_id}` | `asof`, `elm`, `response_format`, `law_full_text_format` |
| 本文をファイルで取得する | `/law_file/{file_type}/{law_id_or_num_or_revision_id}` | `xml`, `json`, `html`, `rtf`, `docx`、必要なら `asof` |
| 図・様式等の添付を取得する | `/attachment/{law_revision_id}` | 本文中の `Fig` の `src` をクエリの `src` に指定 |

## 時点と形式を取り違えない

- 過去時点は対応するAPIの `asof=YYYY-MM-DD` で指定する。本文・ファイルに履歴IDを渡すと `asof` は無視されるため、履歴IDか対象日のどちらを使って版を選んだか明示する。
- `/laws` の `revision_info` が指定時点の版。`current_revision_info` は `asof` と独立した現在以前の最新の版なので、過去の本文の根拠と混同しない。`amendment_law_id` を指定すると `/laws` の `asof` は無視される。
- 公布日、施行期日、データ更新日を区別する。履歴の `current_revision_status` は現時点との比較であり、対象日当時の状態とは限らない。未施行・廃止・経過措置等は取得したメタ情報と本文で確かめる。
- 本文取得は通常 `response_format=json&law_full_text_format=json` を明示する。両形式が異なる場合、`law_full_text` はBase64になる。JSON本文は試行版で、固定した構造を無確認で使い続けない。
- `/laws` と `/keyword` の続きは返却された `next_offset` を使う。未返却またはnullなら終了し、同じ値の再出現時は止めて不整合を報告する。指定ページだけなら全件走査しない。
- HTTPエラーを「該当法令なし」と扱わない。失敗時はステータスとAPIの `code`・`message` を確認する。タイムアウトを設定し、429・一時的な5xxだけ最大2回の再試行とし、`Retry-After` があれば尊重する。400は条件を見直す。
