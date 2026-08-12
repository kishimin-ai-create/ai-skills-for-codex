# Backend Testing Reference

## Test intent

- 小さいテストではModelのbusiness rule、Serviceのorchestration、Repository contractなどを外部から観測できる契約として検証する。
- 大きいテストでは公開API、validation、error mapping、Repository/Infrastructure境界を検証する。
- テスト名は対象、条件、期待結果を示し、Arrange / Act / Assertを明確にする。
- 正常系、異常系、境界値、認証・認可、空状態、Infrastructure failureを仕様に応じて選ぶ。
- 実装詳細、DB内部状態、脆いmock呼び出し順だけを検証しない。

## Test types and scope

| 種類        | サイズ | 範囲                 | 方針                                          |
| ----------- | ------ | -------------------- | --------------------------------------------- |
| Unit        | Small  | 単一関数・クラス     | 外部依存を避け、Repository境界をmockできる    |
| Integration | Medium | レイヤー間連携・DB   | ローカルDBなどを使用し、公開API境界を検証する |
| E2E         | Large  | 利用者の一連のフロー | 重要な経路に限定してブラウザ自動化を使用する  |

Unit / Integration / E2Eはテストの意図と範囲を説明する用語であり、実際の配置・命名・runner設定はリポジトリ定義を優先する。

## Strategy

- 各レイヤーの契約を内側から外側へ検証する。
- 高影響かつ発生確率の高いリスクからカバレッジを改善する。
- UnitではRepository境界をmockし、Integrationでは可能な範囲で実DBなど実際の境界を使用する。
- E2Eは重要な利用者経路に絞り、実行コストと保守性を管理する。

## Verification order

バックエンドディレクトリで対象を絞ったテストを先に実行し、その後に次を順に実行する。

リポジトリが定義するlint、型検査、テストのコマンドをこの順に実行する。コマンド名は言語・ツールチェーンに合わせて読み替え、存在しないコマンドを推測しない。

失敗した場合、test code、implementation、fixture、environmentのどれが原因かを分類する。全体テストを実行していない場合は完了と断定しない。

## Boundary safety

- Test dataを独立させ、テスト間でDB・port・認証状態を共有しない。
- 実在の秘密情報や個人情報をfixtureへ保存しない。
- API境界のテストではstatus codeだけでなくresponse body、error shape、公開されるメッセージを確認する。
- Repository/Infrastructureの実装詳細に依存せず、公開Portと観測可能な結果を検証する。
