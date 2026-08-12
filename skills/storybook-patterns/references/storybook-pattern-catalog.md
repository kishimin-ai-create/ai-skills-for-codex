---
name: storybook-patterns
description: Storybook作成パターン集。StorybookCreatorAgentから参照されるCSF 3.0、MSW、アクセシビリティ、レスポンシブ対応の詳細な実装例をまとめたもの。
---

# Storybook Patterns

## Story Structure (CSF 3.0 Pattern)

### Component Story Template

```tsx
// ComponentName.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { ComponentName } from "./ComponentName";

const meta = {
  title: "Features/ComponentName",
  component: ComponentName,
  parameters: {
    layout: "centered",
  },
} satisfies Meta<typeof ComponentName>;

export default meta;
type Story = StoryObj<typeof meta>;

//  Default state
export const Default: Story = {
  args: {
    // typical prop values
  },
};

//  Interactive variant
export const Hover: Story = {
  args: {
    /* hover-relevant props */
  },
  parameters: {
    pseudo: { hover: true },
  },
};

//  Error state (if component accepts error prop)
export const WithError: Story = {
  args: {
    error: "Validation message",
  },
};

//  Loading state (if component has async behavior)
export const Loading: Story = {
  args: {
    isLoading: true,
  },
};
```

### Page Story Template (with MSW)

```tsx
// PageName.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { http, HttpResponse } from "msw";
import { PageName } from "./PageName";

const meta = {
  title: "Pages/PageName",
  component: PageName,
  parameters: {
    layout: "fullscreen",
    msw: {
      handlers: [
        http.get("*/api/endpoint", () => {
          return HttpResponse.json({
            // mock response
          });
        }),
      ],
    },
  },
} satisfies Meta<typeof PageName>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get("*/api/todos", () => {
          return HttpResponse.json([
            { id: 1, title: "Task 1", completed: false },
          ]);
        }),
      ],
    },
  },
};

export const ErrorState: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get("*/api/todos", () => {
          return HttpResponse.json({ error: "Server error" }, { status: 500 });
        }),
      ],
    },
  },
};

export const Empty: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get("*/api/todos", () => {
          return HttpResponse.json([]);
        }),
      ],
    },
  },
};
```

## Story Variant Checklist

各コンポーネントについて、該当する場合は次のバリエーションを作成する。

### All Components

- [ ] **Default** — 最も一般的なPropsを使った通常状態
- [ ] **Focus** — `focus-visible` が有効な状態（`pseudo: { focus: true }` を使用）
- [ ] **Hover** — ButtonやLinkのHover状態（`pseudo: { hover: true }` を使用）

### Form Components

- [ ] **Default** — 空の状態
- [ ] **Filled** — ユーザー入力済み
- [ ] **Error** — バリデーションエラーメッセージ付き
- [ ] **Disabled** — 無効状態
- [ ] **Loading** — 非同期送信中

### Data Display Components

- [ ] **Default** — 一般的なデータを表示
- [ ] **Empty** — データが存在しない状態
- [ ] **Loading** — データ取得中
- [ ] **Error** — データ取得失敗

### Page-Level Components

- [ ] **Default** — データが正常に取得できた状態
- [ ] **Empty** — データが存在しない状態
- [ ] **Loading** — 初回データ読み込み中
- [ ] **Error** — APIエラー
- [ ] **Mobile** — レスポンシブレイアウト（`sm` ブレークポイント）
- [ ] **Tablet** — レスポンシブレイアウト（`md` ブレークポイント）

### Interactive Components

- [ ] **Default** — 初期状態（閉じている・非アクティブ）
- [ ] **Active** — 展開・アクティブ状態
- [ ] **Disabled** — 無効状態
- [ ] **Keyboard Focus** — キーボードフォーカス状態
- [ ] **Error** — エラー状態（該当する場合）

## Responsive Stories

コンポーネントが画面サイズによってどのように変化するかを示す。

```tsx
// Responsive story example
export const Mobile: Story = {
  args: {
    /* props */
  },
  parameters: {
    viewport: {
      defaultViewport: "iphone12",
    },
  },
};

export const Tablet: Story = {
  args: {
    /* props */
  },
  parameters: {
    viewport: {
      defaultViewport: "ipad",
    },
  },
};
```

## Accessibility Stories

キーボード操作やスクリーンリーダー利用時の動作を確認するStoryを作成する。

```tsx
// Accessibility-focused story
export const KeyboardNavigation: Story = {
  args: {
    /* props */
  },
  render: (args) => (
    <div>
      <p className="text-sm text-gray-600 mb-4">
        Use Tab to navigate. Press Enter or Space to interact.
      </p>
      <ComponentName {...args} />
    </div>
  ),
};

// Focus visible testing
export const FocusVisible: Story = {
  args: {
    /* props */
  },
  parameters: {
    pseudo: { focus: true },
  },
};
```

## MSW Integration

### Example: Component with API call

```tsx
// UserProfile.stories.tsx
import { http, HttpResponse } from "msw";

export const Default: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get("*/api/users/:id", ({ params }) => {
          return HttpResponse.json({
            id: params.id,
            name: "John Doe",
            email: "john@example.com",
            avatar: "https://via.placeholder.com/150",
          });
        }),
      ],
    },
  },
};

export const ApiError: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get("*/api/users/:id", () => {
          return HttpResponse.json(
            { error: "User not found" },
            { status: 404 },
          );
        }),
      ],
    },
  },
};

export const NetworkTimeout: Story = {
  parameters: {
    msw: {
      handlers: [
        http.get("*/api/users/:id", async () => {
          await new Promise((resolve) => setTimeout(resolve, 10000)); // Timeout
          return HttpResponse.json({});
        }),
      ],
    },
  },
};
```

## Tailwind-Specific Stories

コンポーネントがTailwind CSSのレスポンシブユーティリティを利用している場合は、レスポンシブな挙動を確認できるStoryを作成する。

```tsx
// Example: Component with responsive classes
export const ResponsiveLayout: Story = {
  render: (args) => (
    <div className="w-full">
      <p className="text-xs text-gray-500 mb-4">
        Resize viewport to see responsive behavior
      </p>
      <ComponentName {...args} />
    </div>
  ),
};
```
