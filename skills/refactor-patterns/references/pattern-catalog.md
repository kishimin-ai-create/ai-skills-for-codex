---
name: refactor-patterns
description: TypeScriptコードのリファクタリングパターン集。RefactorAgentが使用する詳細なパターン例、アンチパターン、実装例をまとめる。
---

# Refactoring Patterns

## Common Refactoring Patterns

### Pattern 1: Extract Validation Logic (No Behavior Change)

```typescript
// BEFORE: Validation mixed with business logic
async execute(input: CreateAppInput): Promise<CreateAppOutput> {
  if (!input.name || input.name.trim() === "") {
    return { success: false, statusCode: 422, error: {...}, data: null };
  }
  if (input.name.length > 100) {
    return { success: false, statusCode: 422, error: {...}, data: null };
  }
  // ...rest of logic
}

// AFTER: Extracted validation (same behavior, clearer code)
private validateName(name: string): { valid: true } | { valid: false; error: CreateAppOutput } {
  if (!name || name.trim() === "") {
    return {
      valid: false,
      error: { success: false, statusCode: 422, error: {...}, data: null }
    };
  }
  if (name.length > 100) {
    return {
      valid: false,
      error: { success: false, statusCode: 422, error: {...}, data: null }
    };
  }
  return { valid: true };
}

async execute(input: CreateAppInput): Promise<CreateAppOutput> {
  const validation = this.validateName(input.name);
  if (!validation.valid) return validation.error;
  // ...rest of logic (unchanged)
}
```

**Why safe**: 戻り値が同一で、エラーコードも変更されず、処理の流れが維持される。

### Pattern 2: Extract Error Response Factory (Eliminate Duplication)

```typescript
// BEFORE: Error responses repeated throughout
if (!input.name) {
  return {
    success: false,
    statusCode: 422,
    error: { code: "APP_NAME_INVALID", message: "Name required" },
    data: null
  };
}

// AFTER: Centralized error factory
private validationError(code: string, message: string): CreateAppOutput {
  return { success: false, statusCode: 422, error: { code, message }, data: null };
}

// Usage (same behavior, less duplication)
if (!input.name) return this.validationError("APP_NAME_INVALID", "Name required");
```

**Why safe**: 戻り値とエラーコードが同じで、データ構造も変わらない。

### Pattern 3: Rename for Clarity (Preserves All Behavior)

```typescript
// BEFORE: Unclear naming
const result = await this.repo.findByName(input.name);
if (result) {
  /* handle duplicate */
}

// AFTER: Clearer naming (no behavior change)
const existingApp = await this.appRepository.findByName(input.name);
if (existingApp) {
  /* handle duplicate - logic identical */
}
```

**Why safe**: ロジックと振る舞いは同一で、名前だけを変更している。既存テストにも影響しない。

### Pattern 4: Guard Clauses (Improved Readability, No Behavior Change)

```typescript
// BEFORE: Nested if statements
if (isValid) {
  if (isUnique) {
    if (isAuthorized) {
      // Do work
    } else {
      return unauthorized();
    }
  } else {
    return duplicate();
  }
} else {
  return invalid();
}

// AFTER: Early returns (same behavior, better clarity)
if (!isValid) return invalid();
if (!isUnique) return duplicate();
if (!isAuthorized) return unauthorized();
// Do work
```

**Why safe**: 制御フローと戻り値は同一で、ロジックの意味も維持される。

### Pattern 5: Consolidate Similar Error Handling

```typescript
// BEFORE: Repeated error handling patterns
try {
  step1();
} catch (error) {
  return { success: false, statusCode: 500, error: {...} };
}

try {
  step2();
} catch (error) {
  return { success: false, statusCode: 500, error: {...} };
}

// AFTER: Consolidated error handling (same behavior)
const executeSteps = async () => {
  await step1();
  await step2();
};

try {
  await executeSteps();
} catch (error) {
  return { success: false, statusCode: 500, error: {...} };
}
```

**Why safe**: エラー処理の経路と戻り値は同一で、振る舞いも維持される。

## Specific Refactoring Techniques for Backend (Hono + TypeScript)

### Technique 1: Extract Port/Adapter Responsibilities

```typescript
// Move repository-specific logic into repository class
// Move validation into validator class/function
// Keep orchestration in interactor only
```

- Repository固有のロジックをRepositoryクラスへ移動する
- バリデーションをValidatorクラスまたは関数へ移動する
- Interactorにはオーケストレーションのみを残す

### Technique 2: Improve Error Handling in Service Layer

```typescript
// Consolidate try-catch patterns
// Map infrastructure errors to domain errors consistently
// Extract error response building
```

- `try-catch` のパターンを統合する
- インフラストラクチャのエラーをドメインエラーへ一貫して変換する
- エラーレスポンスの生成処理を抽出する

### Technique 3: Organize Usecase Classes

```typescript
// One public method (execute) per interactor
// Private methods for sub-responsibilities
// Clear separation between input validation / business logic / error handling
```

- Interactorごとに公開メソッドを `execute` の1つだけにする
- サブ責務をprivateメソッドへ分離する
- 入力検証、ビジネスロジック、エラーハンドリングを明確に分離する

## Specific Refactoring Techniques for Frontend (React + TypeScript)

### Technique 1: Extract Components (No Behavior Change)

```typescript
// BEFORE: Large component with multiple responsibilities
export function AppCreatePage() {
  // Form input logic
  // Form submission logic
  // Error display logic
  // Loading state logic
}

// AFTER: Extracted components (same behavior, clearer structure)
function AppNameInput({ value, onChange, error }) {
  /* input logic */
}
function ErrorDisplay({ error }) {
  /* error display */
}
function SubmitButton({ loading, onClick }) {
  /* button logic */
}

export function AppCreatePage() {
  // Orchestration only
}
```

大きなコンポーネントから責務ごとに子コンポーネントを抽出する。振る舞いは変えず、構造だけを明確にする。

### Technique 2: Extract Custom Hooks (No Behavior Change)

```typescript
// BEFORE: Form state in component
function AppCreatePage() {
  const [name, setName] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  // ...
}

// AFTER: Extracted hook (same behavior, reusable)
function useAppCreateForm() {
  const [name, setName] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  return { name, setName, error, setError, loading, setLoading };
}

export function AppCreatePage() {
  const form = useAppCreateForm();
  // ...
}
```

コンポーネント内の状態管理をCustom Hookへ抽出する。振る舞いを変えず、再利用可能な構造にする。

### Technique 3: Improve Prop Handling (No Behavior Change)

```typescript
// BEFORE: Magic prop values
<Button onClick={() => handleClick()} disabled={loading} />

// AFTER: Clear intent (same behavior, more readable)
<SubmitButton isLoading={loading} onSubmit={handleSubmit} />
```

意味が分かりにくいPropsを、意図が明確に伝わるPropsへ変更する。

## Anti-Patterns: Things That Look Safe But Aren't

### Anti-Pattern 1: "Just Optimizing" (Without Clarity Improvement)

```typescript
// WRONG - Performance improvement only, no clarity gain
// Original: straightforward loop
// Refactored: complex reduce() just for performance
// Tests pass but you've changed the code intent for one benefit only
```

**Why risky**: 最適化だけを目的とした変更は、振る舞いの違いを隠す可能性がある。保守的に変更する。

### Anti-Pattern 2: "Better Organization" (Changing Behavior)

```typescript
// WRONG - Looks like organization but changes behavior
async execute(input) {
  // Original: validates then checks duplicates
  await validateInput(input);
  const existing = await findByName(input.name);

  // Refactored: introduces early return (changes behavior order!)
  const existing = await findByName(input.name);  // Now before validation
  await validateInput(input);
}
```

**Why risky**: 処理順序の変更は振る舞いに影響する可能性がある。たとえば、本来不要だったデータベース呼び出しが実行される場合がある。

### Anti-Pattern 3: "Adding Comments for Future Devs"

```typescript
// WRONG - Adding explanations as code changes
// Original clean line
const result = await repo.find(id);

// Refactored with "clarity"
// eslint-disable-next-line some-rule
// TODO: This could be optimized by caching
const result = await repo.find(id); // Get from database
```

**Why risky**: コードやコメントという余計な変更が追加されている。リファクタリングは純粋な構造改善に留める。

### Anti-Pattern 4: "Fixing Supposed Bugs" While Refactoring

```typescript
// WRONG - Refactoring + bug fix combined
// Original code (tests pass, so it's correct by definition)
if (status === "open") {
  /* do something */
}

// Refactored: "Fix" - but this changes tested behavior!
if (status === "open" || status === "pending") {
  /* do something */
}
```

**Why risky**: テストが正しさを定義している。テストが通っている状態で、失敗するテストを追加せずに振る舞いを変更してはならない。

## Safety-First Example: CreateAppInteractor Refactoring

**Original Code**（正常に動作し、テストも通っているコード）:

```typescript
export class CreateAppInteractor {
  constructor(private appRepository: AppRepository) {}

  async execute(input: CreateAppInput): Promise<CreateAppOutput> {
    try {
      if (!input.name || input.name.trim() === "") {
        return {
          success: false,
          statusCode: 422,
          error: { code: "APP_NAME_INVALID", message: "App name is required" },
          data: null,
        };
      }

      if (input.name.length > 100) {
        return {
          success: false,
          statusCode: 422,
          error: {
            code: "APP_NAME_INVALID",
            message: "App name must not exceed 100 characters",
          },
          data: null,
        };
      }

      const existing = await this.appRepository.findByName(input.name);
      if (existing) {
        return {
          success: false,
          statusCode: 409,
          error: {
            code: "APP_NAME_DUPLICATE",
            message: `App with name "${input.name}" already exists`,
          },
          data: null,
        };
      }

      const createdApp = await this.appRepository.create({ name: input.name });
      return {
        success: true,
        statusCode: 201,
        data: createdApp,
      };
    } catch (error) {
      return {
        success: false,
        statusCode: 500,
        error: {
          code: "INTERNAL_SERVER_ERROR",
          message: "An unexpected error occurred. Please try again later.",
        },
        data: null,
      };
    }
  }
}
```

**Refactored Code**（より明確になり、既存テストも引き続き通るコード）:

```typescript
export class CreateAppInteractor {
  constructor(private appRepository: AppRepository) {}

  async execute(input: CreateAppInput): Promise<CreateAppOutput> {
    try {
      // Validate input
      const validation = this.validateAppName(input.name);
      if (!validation.isValid) {
        return validation.error;
      }

      // Check uniqueness
      const existing = await this.appRepository.findByName(input.name);
      if (existing) {
        return this.nameConflictError(input.name);
      }

      // Create and return
      const createdApp = await this.appRepository.create({ name: input.name });
      return this.successResponse(createdApp);
    } catch (error) {
      return this.serverErrorResponse();
    }
  }

  private validateAppName(
    name: string,
  ): { isValid: true } | { isValid: false; error: CreateAppOutput } {
    if (!name || name.trim() === "") {
      return {
        isValid: false,
        error: this.validationError("App name is required"),
      };
    }

    if (name.length > 100) {
      return {
        isValid: false,
        error: this.validationError("App name must not exceed 100 characters"),
      };
    }

    return { isValid: true };
  }

  private validationError(message: string): CreateAppOutput {
    return {
      success: false,
      statusCode: 422,
      error: { code: "APP_NAME_INVALID", message },
      data: null,
    };
  }

  private nameConflictError(name: string): CreateAppOutput {
    return {
      success: false,
      statusCode: 409,
      error: {
        code: "APP_NAME_DUPLICATE",
        message: `App with name "${name}" already exists`,
      },
      data: null,
    };
  }

  private successResponse(app: App): CreateAppOutput {
    return {
      success: true,
      statusCode: 201,
      data: app,
    };
  }

  private serverErrorResponse(): CreateAppOutput {
    return {
      success: false,
      statusCode: 500,
      error: {
        code: "INTERNAL_SERVER_ERROR",
        message: "An unexpected error occurred. Please try again later.",
      },
      data: null,
    };
  }
}
```

**Why This Refactoring is Safe**:

- すべてのテストが通る（戻り値とエラーコードが同一）
- 外部から観測できる振る舞いが同一
- バリデーションロジックが明確になる
- エラーハンドリングが統合される
- 保守・拡張しやすくなる
- Repository呼び出しなどの副作用が維持される
- 新しい機能を追加していない
