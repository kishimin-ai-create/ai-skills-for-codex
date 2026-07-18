# Implementation Pattern Catalog

## Pattern 1: Validation First, Then Success or Error

```typescript
async execute(input: InputType): Promise<OutputType> {
  if (!input.name || input.name.trim() === "") {
    return { success: false, statusCode: 422, error: { code: "INVALID_INPUT", message: "Field required" }, data: null };
  }
  if (input.name.length > 100) {
    return { success: false, statusCode: 422, error: { code: "INVALID_INPUT", message: "Too long" }, data: null };
  }
  const existing = await this.repository.findByName(input.name);
  if (existing) {
    return { success: false, statusCode: 409, error: { code: "DUPLICATE", message: "Already exists" }, data: null };
  }
  try {
    const created = await this.repository.create(input);
    return { success: true, statusCode: 201, data: created };
  } catch {
    return { success: false, statusCode: 500, error: { code: "INTERNAL_SERVER_ERROR", message: "Internal server error" }, data: null };
  }
}
```

## Pattern 2: Throw When the Contract Expects Exceptions

```typescript
async execute(input: InputType): Promise<OutputType> {
  if (!input.isValid) throw new ValidationError("Invalid input");
  return this.repository.create(input);
}
```

テストが結果オブジェクトを期待する場合は構造化エラーを返し、契約が例外を期待する場合は型付きエラーを投げる。根拠なく形式を切り替えない。

## Pattern 3: Implement the React Happy Path First

```tsx
export function AppCreatePage() {
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const result = await api.createApp({ name });
      if (result.success) navigate(`/apps/${result.data.id}`);
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to create app");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="name">App Name *</label>
      <input id="name" value={name} onChange={(event) => setName(event.target.value)} disabled={loading} />
      {error && <div role="alert">{error}</div>}
      <button type="submit" disabled={loading}>{loading ? "Creating..." : "Create"}</button>
      <button type="button" onClick={() => navigate("/apps")}>Cancel</button>
    </form>
  );
}
```

コンポーネントテストが検証する状態と操作だけを実装する。

## Example: CreateApp Interactor

テストでは次の要件が想定される。

- 有効な名前 → Appを作成し、Appデータ付きのステータス201を返す。
- 空または空白の名前 → ステータス422と`APP_NAME_INVALID`を返す。
- 100文字を超える名前 → ステータス422と`APP_NAME_INVALID`を返す。
- 重複名 → ステータス409と`APP_NAME_DUPLICATE`を返す。
- 1文字および100文字の名前 → 成功する。
- Repository障害 → ステータス500と汎用エラーメッセージを返す。

```typescript
export interface CreateAppInput { name: string; }

export interface CreateAppOutput {
  success: boolean;
  statusCode: number;
  data: App | null;
  error?: { code: string; message: string };
}

export class CreateAppInteractor {
  constructor(private appRepository: AppRepository) {}

  async execute(input: CreateAppInput): Promise<CreateAppOutput> {
    try {
      if (!input.name || input.name.trim() === "") {
        return { success: false, statusCode: 422, error: { code: "APP_NAME_INVALID", message: "App name is required" }, data: null };
      }
      if (input.name.length > 100) {
        return { success: false, statusCode: 422, error: { code: "APP_NAME_INVALID", message: "App name must not exceed 100 characters" }, data: null };
      }
      const existing = await this.appRepository.findByName(input.name);
      if (existing) {
        return { success: false, statusCode: 409, error: { code: "APP_NAME_DUPLICATE", message: `App with name "${input.name}" already exists` }, data: null };
      }
      const createdApp = await this.appRepository.create({ name: input.name });
      return { success: true, statusCode: 201, data: createdApp };
    } catch {
      return { success: false, statusCode: 500, error: { code: "INTERNAL_SERVER_ERROR", message: "An unexpected error occurred. Please try again later." }, data: null };
    }
  }
}
```

この実装は境界値を検証し、一意性を確認し、テストが検証するレスポンス形式を維持し、Infrastructure障害を変換し、契約外の振る舞いを追加しない。

## Anti-patterns

### Overbuilding Beyond Tests

テストされていないページネーション、合計値、ページ番号、その他のフィールドを追加しない。テストが検証する契約だけを返す。

### Refactoring During Green

振る舞いがGreenになる前にヘルパー抽出やコード再構成を行わない。最小実装を維持し、Refactorフェーズで整理する。

### Hardcoded Rejection

テストが重複検出を要求している場合、`findByName`から常に`null`を返さない。最小限の実際の検索処理を実装する。

### Modifying Tests to Pass

期待値を弱めたり書き換えたりしない（例: 期待する422を400へ変更する）。確立された契約を満たすよう実装を変更する。
