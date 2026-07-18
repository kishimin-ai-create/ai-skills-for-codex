# Security: Architecture and Logging Rules

OWASP ASVS 5.0のアーキテクチャ、依存管理、セキュアコーディング、並行性、ログ、エラー処理（V15、V16）を対象とする。

## Dependency management (V15.2)

- すべての第三者ライブラリについてSoftware Bill of Materials（SBOM）を維持する。
- 依存関係は事前に定義した信頼済みRepositoryからだけ取得し、Dependency Confusion攻撃を防ぐ。
- 脆弱なコンポーネントの修正期限を定義・適用し、文書化した期限内に更新する。
- 本番ビルドへテストコード、サンプル、開発専用機能を含めない。

## Secure coding patterns (V15.3)

- データオブジェクトから必要なフィールドだけを返し、利用者がアクセスできないフィールドを含む完全なオブジェクトを返さない。
- Mass Assignmentを防ぐため、Controllerや操作ごとに書き込み可能フィールドを明示的に許可する。
- JavaScriptでは厳密等価（`===`）と明示的な型検査を使用し、型変換を前提にしない。
- JavaScriptのPrototype Pollutionを防ぐため、動的キーの保存には通常のObjectリテラルではなく`Map`または`Set`を使用する。
- 外部呼び出しは明示的な要件がない限りHTTPリダイレクトを追従しない設定にする。
- HTTPパラメータ汚染を防ぐため、Query String、Body、Cookie、Headerのパラメータを区別し、無条件にマージしない。
- 元のクライアントIPは信頼する単一のHeaderフィールドで伝達し、Rate Limitやログに使う前に検証する。

## Dangerous functionality

- 信頼できないデータのデシリアライズ、Rawバイナリ解析、動的コード実行、直接メモリ操作を行うすべてのコードパスを文書化する。
- 危険な機能をSandbox化、カプセル化、Container化、Network分離し、影響範囲を制限する。
- 保守不良、EOL、CVE履歴のある危険な第三者ライブラリを記録し、代替・隔離・更新計画を持つ。

## Safe concurrency (V15.4)

- マルチスレッドで共有する可変オブジェクトには、スレッドセーフな型とLock・Semaphoreなどの同期を使用する。
- ファイル存在や権限確認と、それに続く操作を原子的に実行し、TOCTOU競合を防ぐ。
- Lockの管理をResource所有者の内部に保ち、外部変更やDeadlockを防ぐ。
- Thread Poolは公平なスケジューリングを使用し、Thread Starvationを防ぐ。

## Security logging (V16)

### 記録するイベント

- すべての認証試行（成功・失敗）と使用した認証方式・要素。
- すべての認可失敗。ASVS L3では、機密データ自体を記録せず、機密データへの全アクセスも記録する。
- 入力検証、業務ロジック、Anti-automationなどSecurity Controlの迂回試行。
- 予期しないエラーとSecurity Controlの失敗（例: Backend TLS失敗）。

### ログ形式 (V16.2)

- timestamp（UTCまたは明示的なTZ offset）、source、actor（誰が）、action（何を）、outcome（結果）を含める。
- Log Processorが扱える機械可読形式（JSON推奨）を使用する。
- すべてのログコンポーネントで時刻源を同期する。

### ログの機密性 (V16.2.5)

- 認証情報、決済情報、その他の機密データを記録しない。
- Session Tokenは保護レベルに応じてハッシュ化または一部マスクした形だけを記録する。

### ログ保護 (V16.4)

- Log Injectionを防ぐため、すべてのログ内容をエンコードする。
- ログを不正アクセスと改ざんから保護する。
- ログを論理的に分離されたシステムへリアルタイム送信し、アプリケーション侵害がログ侵害へ波及しないようにする。

## Error handling (V16.5)

- 予期しないエラーやSecurity Sensitiveなエラーでは、利用者へ汎用メッセージだけを返し、Stack Trace、Query、秘密情報を公開しない。
- 外部Resource障害時も安全に稼働を継続する（Circuit Breaker、Graceful Degradationなど）。
- 例外がFail-openにならないようにする。検証エラーが発生した取引を完了させてはならない。
- 未処理例外を捕捉し、プロセス終了を防ぐ最終Error Handlerを定義する。

## Review evidence

- SBOM、依存供給元、脆弱性修正期限、本番成果物の内容を確認したか。
- Mass Assignment、Prototype Pollution、Parameter Pollution、Redirect追従を検証したか。
- 危険機能の隔離と共有状態の同期、TOCTOU対策を確認したか。
- 認証・認可・制御迂回・エラーのログが、機密情報なしの監査形式で記録されるか確認したか。
- ログへのアクセス制御、改ざん防止、分離送信、障害時のFail-closedを検証したか。
