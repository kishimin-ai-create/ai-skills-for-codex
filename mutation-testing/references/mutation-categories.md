# Mutation Categories

## Conditional Boundary Mutation

境界条件の変更を検出する。

例:

```text
>  → >=
>= → >
<  → <=
<= → <
```

条件値 `N` に対して、原則として以下を検証する。

```text
N - 1
N
N + 1
```

値の性質上適切でない場合は、意味的に同等な境界ケースを選択する。

## Conditional Negation Mutation

条件式の反転を検出する。

例:

```text
== → !=
true → false
false → true
条件式の反転
```

true 側だけでなく、false 側の振る舞いも確認する。

## Arithmetic Mutation

算術演算子の変更を検出する。

例:

```text
+ → -
- → +
* → /
/ → *
% の変更
```

異なる演算でも同じ結果になる入力だけを使用してはならない。

演算の差異を観測できる値を使用する。

悪い例:

```text
100 + 0
100 - 0
```

どちらも `100` になるため、変異を検出できない。

## Value Mutation

値や定数の変更を検出する。

例:

```text
0 → 1
1 → 0
true → false
false → true
定数値変更
引数値変更
閾値変更
```

マジックナンバーが仕様上の意味を持つ場合、その意味をテスト名またはテストケース名から理解できるようにする。

## Statement Mutation

処理の削除や変更を検出する。

例:

```text
statement removal
return removal
function call removal
assignment removal
処理順序変更
```

処理が削除されてもテストが成功する場合は、テスト不足だけでなく、不要なプロダクトコードである可能性も検討する。

## Return Value Mutation

戻り値の変更を検出する。

例:

```text
value → null
value → undefined
value → empty
true → false
false → true
object → empty object
array → empty array
```

戻り値の存在だけを確認してはならない。

戻り値の内容を検証する。
