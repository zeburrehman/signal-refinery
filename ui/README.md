# Signal Refinery UI

A modern, type-safe web application built with Next.js 16, React 19, and TypeScript.

## 🚀 Tech Stack

- **Framework**: [Next.js 16](https://nextjs.org/)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS 4](https://tailwindcss.com/)
- **Runtime**: React 19

## 📁 Project Structure

```
src/
├── app/                 # Next.js App Router pages and layouts
│   ├── layout.tsx      # Root layout with Header and Footer
│   ├── page.tsx        # Home page
│   └── globals.css     # Global styles
├── components/         # Reusable React components
│   ├── Header.tsx
│   ├── Footer.tsx
│   └── ...
├── hooks/             # Custom React hooks
│   └── README.md
├── lib/               # Utility library functions
│   └── index.ts
├── services/          # API services and integrations
│   └── README.md
├── types/             # TypeScript type definitions
│   └── index.ts
├── constants/         # Application constants
│   └── index.ts
├── utils/             # Utility functions
│   └── index.ts
└── middleware.ts      # Next.js middleware

public/
├── images/           # Image assets
├── icons/            # Icon assets
└── fonts/            # Font files
```

## 🛠️ Getting Started

### Prerequisites

- Node.js 18+ (recommended: 20+)
- npm, yarn, pnpm, or bun

### Installation

1. **Start the development server**

```bash
npm run dev
```

2. **Create environment variables** (optional)

```bash
cp .env.example .env.local
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## 📚 Available Scripts

```bash
# Development
npm run dev              # Start development server
npm run build            # Build for production
npm run start            # Start production server

# Quality
npm run lint             # Run ESLint
npm run type-check       # Run TypeScript type checker
npm run format           # Format code with Prettier
```

## 🏗️ Project Features

### Best Practices Included

- ✅ **Type Safety**: Full TypeScript configuration with strict mode
- ✅ **Component Structure**: Organized component directory
- ✅ **Reusable Hooks**: Custom hooks folder for composition
- ✅ **Service Layer**: Dedicated folder for API and external services
- ✅ **Constants**: Centralized application constants
- ✅ **Utilities**: Helper functions organized by purpose
- ✅ **Security Headers**: Configured in next.config.ts
- ✅ **Environment Management**: Example .env file included
- ✅ **Module Paths**: Path aliases configured (@/*)

### Performance Optimized

- Image optimization enabled
- Compression enabled
- Security headers configured
- React Strict Mode enabled

## 🎯 Development Guidelines

### Component Creation

Create components in `src/components/`:

```typescript
// src/components/MyComponent.tsx
export function MyComponent() {
  return <div>Component</div>;
}
```

### Custom Hooks

Place hooks in `src/hooks/`:

```typescript
// src/hooks/useMyHook.ts
export const useMyHook = () => {
  // Hook logic
};
```

### Type Definitions

Define types in `src/types/`:

```typescript
// src/types/index.ts
export type MyType = {
  id: string;
  name: string;
};
```

### Constants

Add constants in `src/constants/`:

```typescript
// src/constants/index.ts
export const MY_CONSTANT = "value";
```

## 🔐 Security

- CSP headers configured
- X-Content-Type-Options enabled
- X-Frame-Options enabled
- Environment variables properly managed

## 📦 Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Docker

Create a `Dockerfile`:

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run type check and formatting
4. Submit a pull request

## 📚 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## 📄 License

MIT License
