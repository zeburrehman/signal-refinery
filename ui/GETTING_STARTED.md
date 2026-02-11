# 🚀 Getting Started with Signal Refinery UI

## Quick Start (2 minutes)

### 1. Start Development Server
```bash
npm run dev
```

### 2. Open in Browser
Navigate to [http://localhost:3000](http://localhost:3000)

You'll see the home page with features and project information.

## 📝 Common Tasks

### Creating a New Component

**File**: `src/components/Button.tsx`
```typescript
export function Button() {
  return (
    <button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
      Click me
    </button>
  );
}
```

**Use it**: `src/app/page.tsx`
```typescript
import { Button } from "@/components/Button";

export default function Home() {
  return <Button />;
}
```

### Creating a Custom Hook

**File**: `src/hooks/useCounter.ts`
```typescript
import { useState } from "react";

export const useCounter = (initialValue = 0) => {
  const [count, setCount] = useState(initialValue);

  return {
    count,
    increment: () => setCount(count + 1),
    decrement: () => setCount(count - 1),
  };
};
```

**Use it**:
```typescript
import { useCounter } from "@/hooks/useCounter";

export function Counter() {
  const { count, increment, decrement } = useCounter();

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}
```

### Adding Type Definitions

**File**: `src/types/index.ts`
```typescript
export type User = {
  id: string;
  name: string;
  email: string;
  role: "admin" | "user";
};

export type Product = {
  id: string;
  name: string;
  price: number;
  inStock: boolean;
};
```

### Creating API Service

**File**: `src/services/api.ts`
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000";

export const fetchUsers = async () => {
  const response = await fetch(`${API_URL}/api/users`);
  if (!response.ok) throw new Error("Failed to fetch users");
  return response.json();
};

export const createUser = async (userData: {
  name: string;
  email: string;
}) => {
  const response = await fetch(`${API_URL}/api/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userData),
  });
  if (!response.ok) throw new Error("Failed to create user");
  return response.json();
};
```

### Adding Constants

**File**: `src/constants/index.ts`
```typescript
export const APP_NAME = "Signal Refinery UI";
export const APP_VERSION = "0.1.0";

export const ROUTES = {
  HOME: "/",
  DASHBOARD: "/dashboard",
  SETTINGS: "/settings",
  ABOUT: "/about",
} as const;

export const API_ENDPOINTS = {
  BASE_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000",
  USERS: "/api/users",
  PRODUCTS: "/api/products",
} as const;

export const PAGINATION = {
  DEFAULT_LIMIT: 10,
  DEFAULT_OFFSET: 0,
} as const;
```

## 🎨 Working with Tailwind CSS

### Styling Components
```typescript
export function Card({ title, children }) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm hover:shadow-md transition-shadow">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">{title}</h2>
      <div className="text-gray-600">{children}</div>
    </div>
  );
}
```

### Responsive Design
```typescript
export function ResponsiveGrid() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div>Column 1</div>
      <div>Column 2</div>
      <div>Column 3</div>
    </div>
  );
}
```

## 🔧 Configuration

### Environment Variables

**Create**: `.env.local`
```bash
NEXT_PUBLIC_API_URL=http://localhost:3000
NEXT_PUBLIC_APP_NAME=Signal Refinery UI
```

**Access in code**:
```typescript
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

### Adding Routes

**Create**: `src/app/dashboard/page.tsx`
```typescript
export default function Dashboard() {
  return <h1>Dashboard</h1>;
}
```

This automatically creates route: `/dashboard`

### Creating Layouts

**Create**: `src/app/admin/layout.tsx`
```typescript
export default function AdminLayout({ children }) {
  return (
    <div className="flex">
      <nav className="w-64 bg-gray-900 text-white p-4">
        Admin Menu
      </nav>
      <main className="flex-1">{children}</main>
    </div>
  );
}
```

## 📚 Project Structure Reference

```
src/
├── app/             → Pages and routes (Next.js)
├── components/      → Reusable React components
├── hooks/           → Custom React hooks
├── lib/             → Library/utility functions
├── services/        → API and external services
├── types/           → TypeScript type definitions
├── constants/       → App constants and config
└── utils/           → Helper utilities
```

## 🚢 Deployment

### Deploy to Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Deploy to Other Platforms

```bash
# Build for production
npm run build

# Start production server
npm run start
```

## 🧪 Quality Assurance

### Type Checking
```bash
npm run type-check
```

### Linting
```bash
npm run lint
```

### Code Formatting
```bash
npm run format
```

## 📖 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)

## ✅ Checklist for New Features

- [ ] Create TypeScript type in `src/types/`
- [ ] Add constant to `src/constants/` if needed
- [ ] Create component(s) in `src/components/`
- [ ] Create API service in `src/services/` if needed
- [ ] Create custom hook in `src/hooks/` if needed
- [ ] Test with `npm run dev`
- [ ] Run `npm run type-check` - no errors
- [ ] Run `npm run build` - successful

## 🆘 Troubleshooting

### Port 3000 already in use?
```bash
npm run dev -- -p 3001
```

### Clear Next.js cache
```bash
rm -rf .next
npm run dev
```

### Type errors?
```bash
npm run type-check
```

### Build fails?
```bash
npm run build -- --debug
```

---

**Happy coding!** 🎉 If you have questions, check the README.md or SETUP_SUMMARY.md files.
