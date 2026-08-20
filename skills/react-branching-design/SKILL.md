---
name: react-branching-design
description: React・TypeScriptの早期return、論理AND、条件演算子、switch、対応表・コンポーネントmapを、表示条件の意味と将来の状態・種別追加から選択・実装・レビューする。loading・error・empty・successなどの状態表示、権限やfeature flag、種別別コンポーネント、入れ子の条件レンダリングを整理するときに使用する。
---

# React Branching Design

現在の分岐数やJSXの短さではなく、条件の意味、排他性、将来の選択肢追加で表現を選ぶ。

## 判断手順

1. 条件を、前提を満たさない状態、真偽値、本質的な二択、名前を持つカテゴリ、動的な構成のいずれかへ分類する。
2. `null`・未対応値・fallback、状態の排他性、アクセシビリティ上必要な表示を仕様とテストから確認する。
3. 次の基準で最小の表現を選ぶ。
4. 利用者から観測できる表示と操作をテストし、構文やコンポーネント内部をassertしない。
5. 状態やカテゴリを追加したときに、既存値とfallbackを混同しないかレビューする。

## 選択基準

### 早期return

コンポーネント本体の前提を満たさない場合や、画面全体を置き換える状態へ使用する。

```tsx
if (query.isPending) return <LoadingView />;
if (query.isError) return <ErrorView error={query.error} />;

return <Profile user={query.data} />;
```

同じ状態モデルを複数箇所の早期returnとJSX内条件へ分散させない。`idle`・`loading`・`success`・`error`のような排他的状態がアプリ自身の契約なら、Discriminated Unionと`switch`を検討する。

### 論理AND（`&&`）

真偽条件に対する「表示する／何も表示しない」へ使用する。

```tsx
return <>{hasError && <FieldError message={message} />}</>;
```

左辺に数値や文字列を直接置かない。`count && <Badge />`は`count`が`0`のとき`0`を描画し得るため、`count > 0`のようにbooleanへする。

### 条件演算子

概念上増加しない二択で、両方の表示が同じ局所的な位置を占める場合に使用する。

```tsx
return <StatusText>{isOnline ? "Online" : "Offline"}</StatusText>;
```

言語、状態、種別、権限など、現在2値でも追加され得るカテゴリには使用しない。条件演算子を入れ子にしない。

### switch

小さく固定されたカテゴリやDiscriminated Unionの表示へ使用する。サポート値とfallbackを明示する。

```tsx
function renderStatus(status: Status) {
  switch (status.kind) {
    case "loading":
      return <LoadingView />;
    case "success":
      return <ResultView result={status.result} />;
    case "error":
      return <ErrorView error={status.error} />;
    default:
      return assertNever(status);
  }
}

function assertNever(value: never): never {
  throw new Error(`Unsupported status: ${String(value)}`);
}
```

外部入力は`unknown`として境界で検証してから、閉じたUnionへ変換する。型アサーションで網羅性を捏造しない。

### 対応表・コンポーネントmap

対応がデータとして構成される、複数箇所で同じ対応を使う、またはpluginのように動的に登録される場合に使用する。

```tsx
const iconByStatus = {
  success: CheckIcon,
  error: AlertIcon,
} satisfies Record<StatusKind, ComponentType<IconProps>>;

const Icon = iconByStatus[statusKind];
return <Icon aria-hidden="true" />;
```

小さな固定集合を短く見せるためだけに導入しない。mapから取得したコンポーネントはPascalCase変数へ代入して描画し、キーの欠落は`satisfies Record<...>`で検出する。

## レビュー規則

- `value === oneCase ? A : B`を見つけたら、`B`が本当の一値か、他のサポート値とfallbackをまとめていないか確認する。
- `condition &&`の左辺がbooleanであり、`0`や空文字を意図せず描画しないことを確認する。
- loading・error・empty・successの条件が複数のbooleanとして同時成立しないか確認する。
- `switch`の`default`へ、明示すべきサポート値を流さない。閉じたUnionでは`never`で網羅性を検査する。
- 分岐からHookを条件付きで呼び出さない。Hookは分岐より前に同じ順序で呼び出すか、責務ごとにコンポーネントを分ける。
- 構文変更のために表示、フォーカス、読み上げ、イベント処理を変えない。既存テストをGreenに保つ。

## テスト

- サポートする各状態・カテゴリとfallbackを個別に検証する。
- 表示テキスト、role、accessible name、利用者操作後の状態遷移をassertする。
- JSX構造、条件式、mapの存在など実装詳細をassertしない。
- カテゴリ追加時は型、分岐、表示文言、Story、テストを一緒に更新する。

## 関連判断

- `$HOME/.codex/docs/adr/0029-use-switch-for-extensible-category-mappings.md`
