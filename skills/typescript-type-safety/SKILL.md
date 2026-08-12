---
name: typescript-type-safety
description: TypeScriptでasによる型アサーションとanyの使用を避け、型ガードとunknownによる安全な型処理を行うための実装ルール。
---

# Typescript Type Safety

## 目的

`as` と `any` を避け、型ガードと `unknown` を使用して型安全なコードを実装すること。

## 手順

### 1. `as` を使用しない

`as` を使用した型アサーションは禁止する。

型アサーションがどうしても必要な場合は、直前の行にコメントを必ず追加する。

```ts
// NG
const el = document.getElementById("app") as HTMLDivElement;

// OK — getElementById は null を返す可能性があるが、この要素は index.html に必ず存在する
const el = document.getElementById("app") as HTMLDivElement;
```

### 2. `any` を使用しない

`any` 型の使用は禁止する。

`any` がどうしても必要な場合は、直前の行にコメントを必ず追加する。

```ts
// NG
function parse(raw: any) { ... }

// OK — この外部ライブラリには型定義が存在しないため、一時的に any を使用する。型定義が追加されたら unknown に置き換える
function parse(raw: any) { ... }
```

### 3. 代替手段を使用する

`as` または `any` を使用する前に、以下の方法を検討する。

- `as` の代わりに型ガード関数（`instanceof`、`typeof`、カスタム型述語）を使用する。
- `any` の代わりに `unknown` を使用し、型ガードによって型を絞り込む。
- 型が本当に不明な場合は、`unknown` → 型ガード → 具体的な型、という流れで安全に処理する。
