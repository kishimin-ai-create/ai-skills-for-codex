---
name: storybook-patterns
description: UIコンポーネントをStorybookで状態網羅、操作、MSW、アクセシビリティ、レスポンシブ、Visual Regressionまで再現可能に設計・実装・レビューするときに使用する。
---

# Storybook Patterns

Storybookを「見た目のサンプル」ではなく、公開API・状態・ユーザー操作・外部境界の実行可能な契約として設計する。対象はReactに限定せず、採用フレームワークとStorybookのバージョンを先に確認する。

## 実行手順

1. 対象コンポーネントの公開props、イベント、非同期境界、テーマ、ロケール、レスポンシブ要件と既存のStorybook設定を確認する。
2. CSF 3.0の`Meta`/`StoryObj`を使い、`satisfies`で型を検査する。`title`、`component`、必要最小限の`args`/`argTypes`を定義する。
3. Defaultに加え、仕様上意味のあるLoading、Empty、Error、Disabled、Validation、長い文言、境界値を独立Storyとして列挙する。1つのStoryに全状態を詰め込まない。
4. `decorators`はproviders・テーマ・レイアウトなど再現に必要な範囲だけに限定し、Story専用の本番分岐を作らない。
5. `play`では`getByRole`、`getByLabelText`、`getByText`など利用者に見える契約で操作し、クリック、キーボード、フォーカス復帰、イベント、エラー表示を`expect`で検証する。
6. HTTP境界はMSWでモックする。成功、空、遅延、4xx/5xx、再試行、キャンセルを固定データで再現し、実API・秘密情報・共有環境に依存させない。
7. `@storybook/addon-a11y`のaxe検査に加え、キーボード順序、フォーカス可視性、名前・説明、色に依存しない状態を確認する。axeで検出できない読み上げは手動確認として記録する。
8. viewport（mobile/desktop）、light/dark、RTL、長い翻訳、縮小モーションを必要なStoryで検証する。日時・乱数・タイムゾーン・フォント・アニメーションはVisual Regression用に固定する。
9. 型チェック、Lint、Storybook build、interaction/テストランナー、a11y、Visual RegressionをCIで実行し、失敗時のtrace・スクリーンショット・レポートを保存する。

## 品質基準

- Story名とargsだけで、再現する状態と前提が判別できる。
- 実装詳細のDOMセレクター、無条件のsnapshot更新、環境依存の実API接続を避ける。
- APIエラー時の再試行・キャンセル、フォームの送信中、空データ、境界値を省略しない。
- Visual Regressionの差分は原因を確認してから更新し、しきい値緩和で問題を隠さない。
- 新しい制約・未確定事項・手動確認をStoryまたはレビュー記録に残す。

## 参照資料

- [既存パターン完全版](references/storybook-pattern-catalog.md)
- [状態とStoryの選択ガイド](references/decision-guide.md)
- [レビュー・完了チェックリスト](references/review-checklist.md)

## 出力契約

変更時は、対象Story一覧、状態網羅表、play/MSW/a11yの検証内容、実行したコマンドと結果、残存リスクを報告する。コードを変更しない計画作成では、推奨構成と未確定事項を明示する。
