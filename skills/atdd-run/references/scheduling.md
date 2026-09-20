# ATDD を継続的に回す手段

セッション内で回すか、セッションを越えて回すかで手段が変わる。

## 選択肢の比較

|  | Cloud Routines | Desktop scheduled task | `/loop` | `/goal` |
| --- | --- | --- | --- | --- |
| 実行場所 | クラウド | このマシン | このマシン | このマシン |
| マシン起動が必要 | 不要 | 必要 | 必要 | 必要 |
| セッション常駐が必要 | 不要 | 不要 | **必要** | **必要** |
| 再起動後も維持 | 維持 | 維持 | `--resume` で復元 | `--resume` で復元 |
| ローカルファイル | **不可（fresh clone）** | 可 | 可 | 可 |
| 最小間隔 | 1時間 | 1分 | 1分 | 間隔ではなく条件 |
| 次のターンの契機 | cron | cron | 時間経過 | 前ターンの終了 |

`CronCreate` / `CronList` / `CronDelete` はセッション内メモリのみで、Claude 終了で消え、
7日で失効する。**恒久的な定期実行には使えない。**

## 使い分け

### 作業中に条件達成まで回す → `/goal`

毎ターン終了時に小型モデルが条件を判定し、未達なら次のターンへ進む。

```text
/goal docs/ACCEPTANCE.md の全ACにチェックが入り、
bun run lint、bun run typecheck、bun run test:coverage:pr、bun run e2e:medium を
実行していずれも終了コード0であることを出力で示す。
実装フェーズで acceptance/ を変更せず、毎ターン
git status --porcelain -- acceptance/ が空であることを出力で示す。
30ターンを超えたら停止する。
```

判定モデルは**コマンドを実行せずファイルも読まない**。会話に現れた出力だけで判定するため、
検証コマンドを実際に実行し、その出力をターン内に残すこと。

Agentをバックグラウンド実行している間は、そのターンの判定が見送られる。
atdd-agent が tdd-agent を起動する構成では判定間隔が延びる。

ターン上限の節を入れないと、達成か不能と判定されるまで回り続ける。

### セッションを開けたまま定期的に再開する → `/loop`

`.claude/loop.md` があれば、引数なしの `/loop` はその内容を実行する。
ATDDの再開手順を書いておけば、中断した作業を拾って続ける。

```text
/loop            # 間隔はClaudeが動的に決める
/loop 30m        # 30分ごと
```

7日で失効する。`Esc` で停止できる。

### マシンを起動しておけば無人で回す → Desktop scheduled task

ローカルファイルへアクセスでき、セッションを開けておく必要がなく、再起動後も維持される。
**ATDDの定期実行にはこれが適する。** デスクトップアプリから作成する。

### CI から回す → GitHub Actions ＋ headless

```bash
claude -p "/atdd-run docs/requirements.md" \
  --permission-mode acceptEdits \
  --permission-prompts none \
  --output-format stream-json --verbose
```

- `-p` でもユーザー起動の Skill は使える（`/skill-name` をプロンプトに含めると展開される）
- `--permission-prompts none` は無人実行用。応答できる人が居ないとき、
  プロンプトが必要な操作は待たずに拒否される
- `--continue` / `--resume <session-id>` で前回の続きから再開できる

Cloud Routines はローカルファイルを持たず fresh clone で動くため、
workerd や Playwright のブラウザを要するこのプロジェクトのテストには適さない。

## 無人実行の前提

| 前提 | 確認方法 |
| --- | --- |
| 権限モード | `permissions.defaultMode` が `bypassPermissions` か `acceptEdits` |
| hooks が有効 | `disableAllHooks` が未設定（`/goal` はhooksの上に実装されている） |
| 進捗が会話外に残る | `docs/ACCEPTANCE.md` のチェックボックスとgitのコミット |

3つ目が最も重要。会話履歴だけに進捗がある状態では、セッションが変わった時点で再開できない。
