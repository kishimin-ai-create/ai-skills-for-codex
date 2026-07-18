---
name: fix-patterns
description: Bug修正パターン集。FixAgentで利用される代表的な修正パターン、チェックリスト、アンチパターンをまとめたもの。
---

# Fix Patterns

## Common Fix Patterns

### Pattern 1: Wrong Status Code / Error Code

```typescript
// BEFORE: Returns 500 instead of 409 for duplicate
catch (error) {
  return { success: false, statusCode: 500, error: { code: "SERVER_ERROR" } };
}

// AFTER: Correct status code for the specific error type
catch (error) {
  if (error instanceof DuplicateError) {
    return { success: false, statusCode: 409, error: { code: "CONFLICT" } };
  }
  return { success: false, statusCode: 500, error: { code: "SERVER_ERROR" } };
}
```

**Why correct**：仕様では重複時は `409` を返すことが求められている。`500` は例外処理の振り分けが誤っていたため発生していた。

---

### Pattern 2: Missing Null Guard

```typescript
// BEFORE: Crashes when repository returns null
const app = await this.appRepository.findById(id);
return { success: true, data: app.toDto() }; // TypeError if null

// AFTER: Correct null handling
const app = await this.appRepository.findById(id);
if (!app) {
  return { success: false, statusCode: 404, error: { code: "NOT_FOUND" } };
}
return { success: true, data: app.toDto() };
```

**Why correct**：Nullチェックが不足していたため実行時エラーになっていた。仕様では `404` を返す必要がある。

---

### Pattern 3: Wrong Validation Logic

```typescript
// BEFORE: Allows empty string after trim
if (input.name === "") {
  return validationError("Name is required");
}

// AFTER: Correctly rejects whitespace-only input
if (!input.name || input.name.trim() === "") {
  return validationError("Name is required");
}
```

**Why correct**：仕様では「前後の空白を除去して判定する」ため、Trim後に空文字になる入力は無効である。

---

### Pattern 4: Missing JSDoc (Rule Violation Fix)

```typescript
// BEFORE: Exported function without JSDoc (violates typescript.instructions.md)
export function createAppController(usecase: AppUsecase): AppController {
  // ...
}

// AFTER: JSDoc added
/**
 * Creates an AppController bound to the given use case.
 */
export function createAppController(usecase: AppUsecase): AppController {
  // ...
}
```

**Why correct**：ルールで、すべてのExportされたFunctionにはJSDocが必須となっている。

---

### Pattern 5: Incorrect Import Path / Missing Export

```typescript
// BEFORE: Import path resolves to wrong module
import { AppError } from "../models/errors";

// AFTER: Correct path
import { AppError } from "../domain/app-error";
```

**Why correct**：ファイル移動後にImport先が更新されていなかった。

---

### Pattern 6: Runtime Boundary Bug Hidden Behind HTTP 200

```text
Symptom: API request returns 200, but the UI shows empty data or an error.
Check:
1. Call the backend endpoint directly.
2. Call the frontend proxy endpoint.
3. Parse both response bodies as JSON.
4. Open the browser UI and verify the user-visible state.
```

**Why correct**：ProxyやCDN、RuntimeではStatus Codeが `200` のままでも、Bodyが欠落・再エンコード・誤転送されることがある。Bodyが正しくParseでき、UIが期待どおり描画されることまで確認して初めて修正が証明される。

---

### Pattern 7: Self-Referential Frontend Proxy Configuration

```text
Symptom: Browser network panel shows frontend-origin /api requests.
Correct interpretation: This is normal for a Next.js route proxy.
Actual check: Verify whether the server-side backend target also points to the
frontend origin. That is the bug.
```

**Why correct**：ブラウザから見えるOriginだけを見て判断すると、正常なBFF/Proxy構成と設定ミスによるループを混同してしまう。

---

### Pattern 8: Timestamp Display Drift

```typescript
new Intl.DateTimeFormat("ja-JP", {
  dateStyle: "medium",
  timeStyle: "short",
  timeZone: "UTC",
});
```

**Why correct**：APIやDatabaseのTimestampはUTCであることが多い。UIでも同じ値を表示したい場合は、ブラウザによる暗黙のTimezone変換を無効化し、描画結果をテストで保証する必要がある。

---

### Pattern 9: Missing Auth Exit Path

```text
Symptom: Login stores a token, but there is no visible logout.
Fix direction: Connect the existing token clearing function to navigation and
test that storage is cleared and the visible navigation changes.
```

**Why correct**：認証はライフサイクル全体で考える必要がある。Loginだけ確認すると、ユーザーはStorageを手動で削除するまでログアウトできない。

---

### Pattern 10: Missing List Pagination State

```text
Symptom: A list renders records but the user cannot move to later pages, or the
request always uses page=1 after interactions.
Fix direction: Keep page state at the page/container boundary, pass page/pageSize/
totalCount to the list component, and reset page to 1 when filters change.
```

**Why correct**：PaginationはQuery Contractの一部である。`totalCount` があってもPage遷移がなければ、2ページ目以降のデータは見えないままになる。

---

### Pattern 11: Scoped Loading Used for Full-Page Loading

```text
Symptom: Initial page loading shows a small inline message or spinner even though
the UI spec requires a full-page branded loading state.
Fix direction: Check the UI specification first. For initial page loads, render a
role="status" full-page overlay with the service logo centered. For refetches
inside an already-rendered page, keep the loading state scoped.
```

**Why correct**：初回Loadingと部分的な再取得ではUX要件が異なる。同じ扱いにすると仕様違反となり、Loading画面も未完成に見えてしまう。

---

### Pattern 12: Locale Drift in Loading and Browser Chrome

```text
Symptom: Visible page copy switches locale, but loading text, logo alt text, or
the browser tab title remains in the default language.
Fix direction: Remove direct imports of default-locale messages from render
paths. Render loading states through the same i18n provider as normal content,
and verify document.title changes with the selected service name.
```

**Why correct**：Loading画面やBrowser Tabもユーザーが見るUIである。ここだけデフォルト言語のままだと、多言語対応が不完全に見える。

## Pre-Fix Checklist

修正を始める前に確認する。

- [ ] 根本原因（症状ではなく原因）が特定できている
- [ ] 正しい挙動が仕様またはルールで確認できている
- [ ] Bugを再現するFailするTestを書いた
- [ ] Testを実行し、REDでFailすることを確認した
- [ ] どのTestがなぜFailしているのか理解している
- [ ] 最小限の変更内容を特定した
- [ ] Proxy/DeploymentのBugでは、Backend出力・Frontend Proxy出力・JSON Parse・UI表示をすべて比較した
- [ ] Frontend `/api` に関する問題では、ブラウザ側Originを疑う前にServer側Proxy Targetを確認した
- [ ] TimestampのBugでは、API/Database値と描画結果をTimezoneを明示して比較した
- [ ] AuthのBugでは、Tokenの保存と削除の両方を確認した
- [ ] ListのBugでは、`page`・`pageSize`・`totalCount`・FilterがUIからAPIまで正しく伝播していることを確認した
- [ ] Loading UIでは、初回LoadingとScoped Loadingの仕様を確認した
- [ ] i18nでは、Loading Text・画像のAlt Text・Browser Tab Titleを対象Localeすべてで確認した
- [ ] Protected Pathが変更対象に含まれていないことを確認した
- [ ] 不具合に直接関係するもの以外の既存TestはすべてPassしている

## Post-Fix Checklist

修正後に確認する。

- [ ] 新しく追加したTestがGREENになった
- [ ] Bugが解消され、症状が再現しない
- [ ] すべてのTestがPassしている（Regressionなし）
- [ ] TypeScriptがエラーなくCompileできる
- [ ] LintがエラーなくPassする
- [ ] 変更は最小限である
- [ ] 新機能や不要な挙動変更を追加していない
- [ ] リファクタリングを行った場合でも、修正対象コードの範囲内に限定している
- [ ] 修正内容とTestを同じCommitで確認・Commitした

## Anti-Patterns: Things That Look Like Fixes But Aren't

### Anti-Pattern 1: "Fix + Cleanup" in One Commit

```typescript
// WRONG - Bug fix bundled with unrelated rename
// Fix: corrected null guard
// Also renamed: appRepo → appRepository (unrelated)
```

**Why risky**：1つのCommitに複数の変更を含めると、Bug修正だけを切り戻せなくなる。修正は必ずAtomicに行う。

---

### Anti-Pattern 2: Rewriting Instead of Fixing

```typescript
// WRONG - Complete rewrite to fix one validation bug
// Original: 80-line function, one validation condition wrong
// "Fixed": entire function rewritten from scratch

// RIGHT - Targeted fix
// Original: 80-line function
// Fixed: changed 1 condition on line 12
```

**Why risky**：全面的な書き換えは、それまで正常だったコードにも新たなBugを持ち込む。

---

### Anti-Pattern 3: Fixing Without Understanding Root Cause

```typescript
// WRONG - Trial-and-error fix
// Test fails with "Cannot read property 'id' of undefined"
// "Fix": added ?. everywhere (nullish chaining spray)
app?.id ?? ""; // was app.id
user?.name ?? ""; // was user.name (user is always defined)
```

**Why risky**：Optional Chainingでエラーを隠すだけでは根本原因は解決されず、予期しない挙動変更につながる。

---

### Anti-Pattern 4: Over-fixing (Fixing More Than Reported)

```typescript
// WRONG - User asked to fix error code; agent also "fixed" error messages,
// added new validation, restructured error handling, etc.
```

**Why risky**：依頼範囲を超えた変更は、十分にテストされていないRegressionを生みやすい。
