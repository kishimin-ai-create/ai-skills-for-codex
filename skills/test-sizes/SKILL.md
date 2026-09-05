---
name: test-sizes
description: GoogleのSmall、Medium、Large定義に基づき、テストが実際に使うネットワーク、DB、ファイルシステム、外部システム、並行性などからサイズを分類し、命名とCIのsize filterを決めるときに使用する。
---

# Test Sizes

テストの種別名や対象範囲ではなく、実行時に使用する資源と制約からSmall、Medium、Largeを判定する。プロジェクトが別の定義を明示している場合は、プロジェクト固有の定義を優先する。

## Google Testing Blogの基準

次の表は、Google Testing Blog「Test Sizes」の原表を日本語で整理したものである。原表の値と判定項目を変えてはならない。

| 特性 | Small | Medium | Large |
| --- | --- | --- | --- |
| ネットワークアクセス | 不可 | localhostのみ | 可 |
| データベース | 不可 | 可 | 可 |
| ファイルシステムアクセス | 不可 | 可 | 可 |
| 外部システムの使用 | 不可 | 非推奨 | 可 |
| 複数スレッド | 不可 | 可 | 可 |
| sleep文 | 不可 | 可 | 可 |
| システムプロパティ | 不可 | 可 | 可 |
| 制限時間（秒） | 60 | 300 | 900以上 |

出典: [Google Testing Blog: Test Sizes](https://testing.googleblog.com/2010/12/test-sizes.html)

## 判定原則

- `Unit`、`Integration`、`E2E`はテストの目的や範囲を説明する名前であり、サイズではない。
- 複数のクラス、モジュール、Provider、Router、コンポーネントを統合しても、それだけではMediumにしない。
- Playwright、MSW、Vitestなど、使用ツールの名前だけでサイズを決めない。
- 実行時間だけでサイズを決めない。表の資源制約を先に判定し、制限時間も満たすサイズを選ぶ。
- 複数の条件に該当する場合は、使用する全資源を許可する最小のサイズを選ぶ。

## 判定手順

1. テストが実際に行うネットワークアクセスを確認する。
   - ネットワークを使用しないなら、この項目ではSmallのままにする。
   - localhostへ接続するなら、少なくともMediumにする。
   - localhost以外へ接続するならLargeにする。
2. DB、ファイルシステム、外部システム、複数スレッド、sleep、システムプロパティの使用を列挙する。
3. 表でSmallに許可されていない資源を1つでも使う場合、Smallに分類しない。
4. 外部システムを使用する場合は原則Largeとする。Mediumでの利用は出典上「非推奨」であるため、例外的に採用するなら、制御方法、隔離性、失敗時の切り分け、Largeにしない理由を記録する。
5. すべての資源条件を満たす最小サイズを選び、そのサイズの制限時間を適用する。

## HTTPモックの判断

「HTTPを扱う」という説明だけではネットワークアクセスの有無を判定できない。実際にソケット通信が発生するかを確認する。

- MSWなどがリクエストを実ネットワークへ出る前に同一プロセス内で捕捉し、DB、ファイルシステム、外部システム、複数スレッド、sleep、システムプロパティも使用しない場合はSmallである。
- localhostで起動したHTTPサーバーへ実際に接続する場合はMediumである。
- localhost以外のAPIや実サービスへ接続する場合はLargeである。

モック対象がHTTPであることや、複数モジュール間の状態遷移を検証すること自体をMediumの根拠にしてはならない。

## ファイル命名

リポジトリ固有の規則を優先する。規則が未定義なら、サイズをファイル名へ明示する。

- C#: `SubjectSmallTests.cs` / `SubjectMediumTests.cs` / `SubjectLargeTests.cs`
- TypeScript: `subject.small.test.ts` / `subject.medium.test.ts` / `subject.large.test.ts`

1ファイルへ異なるサイズのテストを混在させない。`Unit`、`Integration`、`E2E`はテストの目的を説明するために併用できるが、サイズ表記の代わりにはしない。

## CI実行計画

リポジトリが別のスケジュールを明示していない場合は、次の累積スケジュールを使用する。

| サイズ | 実行イベント |
| --- | --- |
| Small | push、pull_request、nightly（schedule）、workflow_dispatch |
| Medium | pull_request、nightly（schedule）、workflow_dispatch |
| Large | nightly（schedule）、workflow_dispatch |

Smallはpushから、MediumはPull Requestから、Largeはnightlyまたは手動実行から対象に加える。後の段階では、それ以前に対象となった小さいサイズも実行する。

1. workflow内でtest runnerを起動するstepをすべて列挙する。通常テストだけでなく、coverage、reporting、mutationなども含める。
2. push、Pull Request、nightly、手動実行ごとに、上記の累積スケジュールまたはプロジェクトが明示したスケジュールを確認する。
3. test runnerを起動する各stepへ、イベントで許可されたサイズだけを選ぶfilterまたはtag条件を適用する。
4. coverageが全サイズを必要とする場合も、高頻度イベントのfilterを外さず、全体coverage用の低頻度jobを別に設計する。
5. 通常テストのmatrixと、テストを起動する補助jobのfilterを別々に検証する。

CIの実行頻度はGoogle Testing Blogの分類表には含まれない。対象リポジトリのADR、CI設定、運用要件が上記と異なるスケジュールを明示している場合は、プロジェクト固有の決定を優先する。
