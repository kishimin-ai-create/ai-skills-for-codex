---
name: test-sizes
description: テストをSmall、Medium、Largeへ分類し、依存範囲・実行環境・失敗の隔離性に基づいてファイル命名、配置、CIのイベント別実行計画、coverageなど補助jobのsize filterを決めるときに使用する。
---

# Test Sizes

サイズは実行時間だけでなく、依存範囲、ネットワーク・DB・ブラウザの有無、並列性、失敗の診断容易性で決める。プロジェクトが別の定義を持つ場合はそちらを優先する。

| サイズ | 依存                                     | 目的                         | 代表的な実行         |
| ------ | ---------------------------------------- | ---------------------------- | -------------------- |
| Small  | 単一プロセス、外部I/Oなし                | 分岐・計算・契約の高速確認   | PRごと、並列         |
| Medium | 複数モジュール、制御されたDB/HTTP        | 境界統合と状態遷移           | PRまたはマージ       |
| Large  | 実ブラウザ、実サービス相当、複数プロセス | ユーザージャーニーと本番近似 | CI・夜間・リリース前 |

## 判定手順

1. 外部I/O、ブラウザ、プロセス、データセット、認証を列挙する。
2. 最小サイズで契約を証明できるなら小さいサイズを選ぶ。
3. サイズを上げる場合は、低層で代替できない理由と実行頻度を記録する。
4. 各テストにサイズをタグ・ディレクトリ・命名規則で付け、CIの選択条件と一致させる。
5. flaky、timeout、環境依存をサイズのせいにせず、原因を分離して修正する。

## ファイル命名

リポジトリ固有の規則を優先する。規則が未定義なら、テストサイズをファイル名とクラス名へ明示する。

- C#: `SubjectSmallTests.cs` / `SubjectMediumTests.cs` / `SubjectLargeTests.cs`
- TypeScript: `subject.small.test.ts` / `subject.medium.test.ts` / `subject.large.test.ts`

1ファイルへ異なるサイズのテストを混在させない。対象が同じでも依存境界が異なる場合は、サイズごとにファイルを分ける。`Unit`や`Integration`は目的の説明に使い、サイズ表記の代わりにしない。

## CI実行計画

1. workflow内でtest runnerを起動するstepをすべて列挙する。名前が`test`のjobだけでなく、coverage、reporting、mutationなども確認する。
2. Pull Request、push、schedule、手動実行ごとに許可するテストサイズを決める。
3. test runnerを起動する各stepへ、イベントで許可されたサイズだけを選ぶfilterまたはtag条件を適用する。
4. coverageが全サイズを必要とする場合は、高頻度イベントのfilterを外さず、全体coverage用の低頻度jobを別に設計する。
5. workflowの静的guardを置く場合は、通常テストのmatrixと補助jobのfilterを別々に検証し、guard自体もCIから実行する。

通常テストだけがサイズ分離されていても、別のstepがfilterなしでtest runnerを起動するなら実行計画は成立していない。CIのjob名や成果物ではなく、実際に起動されるすべてのテストを基準に判定する。

## 参照
