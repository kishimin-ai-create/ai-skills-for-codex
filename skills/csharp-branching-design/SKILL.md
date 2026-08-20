---
name: csharp-branching-design
description: C#の条件演算子、switch文・switch式、Dictionaryによる対応表を、分岐の意味と将来の選択肢追加から選択・実装・レビューする。言語、種別、状態、エラー分類などのカテゴリ対応や、二項演算子が拡張性を隠していないかを判断するときに使用する。
---

# C# Branching Design

分岐の現在の件数ではなく、概念上の選択肢が固定か増加し得るかで構文を選ぶ。

## 判断手順

1. 分岐対象が真偽値、本質的な二択、名前を持つカテゴリ、動的なデータのどれかを特定する。
2. サポート値、未対応値、`null`、fallbackの契約を仕様とテストから確認する。
3. 次の基準で最小の構文を選ぶ。
4. 対応する各入力とfallbackを振る舞いテストで固定する。
5. 将来値を追加したときに、既存値と未対応値を混同しないかレビューする。

## 選択基準

### 条件演算子

本質的に増加しない二択へ使用する。

```csharp
return isEnabled ? enabledValue : disabledValue;
```

言語、状態、種別など、現在2値でも追加され得るカテゴリには使用しない。

### switch

小さく固定されたカテゴリ対応へ使用する。サポート値とfallbackを別々のarmで明示する。

```csharp
return languageCode switch
{
    "ja" => ApiLanguage.Japanese,
    "en" => ApiLanguage.English,
    _ => ApiLanguage.Japanese,
};
```

カテゴリ追加時はenum、対応arm、関連データ、仕様、テストを一緒に更新する。

### Dictionary

対応がデータとして構成される、実行時に差し替わる、または十分大きく検索として扱う場合に使用する。小さな固定集合を短く見せるためだけに導入しない。

## レビュー規則

- `value == oneCase ? resultA : resultB`を見つけたら、`resultB`が本当の一値か、他のサポート値とfallbackをまとめていないか確認する。
- 条件演算子の入れ子でカテゴリを増やさない。
- `switch`の`_`へ、明示すべきサポート値を意図せず流さない。
- 構文変更のために振る舞いを変えない。既存テストをGreenに保つ。

## 関連判断

- `$HOME/.codex/docs/adr/0029-use-switch-for-extensible-category-mappings.md`
