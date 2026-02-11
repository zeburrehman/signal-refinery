# Project Instructions

## Code Style & Conventions

- Use TypeScript strict mode
- Prefer functional components with hooks in React
- Use absolute imports from `@/` alias
- Follow ESLint rules defined in .eslintrc.json

## Architecture

- Keep components in `src/components/`
- API calls go in `src/services/`
- Custom hooks in `src/hooks/`
- Utils in `src/utils/`

## Development Workflow

- Always run `npm run lint` before committing
- Write tests in `.test.tsx` files
- Use shadcn/ui components for UI

## Things to Avoid

- Don't modify package.json without asking
- Don't commit node_modules
- Don't use inline styles (use CSS modules or Tailwind)

## Project Context

- This is a Next.js 15 app with App Router
- Database is PostgreSQL via Prisma
- Auth uses NextAuth v5
- UI is built with shadcn/ui and Tailwind CSS

## Authorization

- You can commit changes directly (use /commit)
- Don't force push to main without explicit approval
- Ask before modifying CI/CD workflows

## Important Notes

- The project uses signal-based state management
- Be aware of stale closures in effects
