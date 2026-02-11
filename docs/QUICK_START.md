# Quick Start Guide

## 🚀 Get Running in 30 Seconds

### With Docker (Recommended)
```bash
docker-compose up
```

Then open:
- **Frontend:** http://localhost:3000
- **Backend Docs:** http://localhost:8000/docs
- **Database:** PostgreSQL on `localhost:5432`

### Without Docker

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

**Frontend:**
```bash
cd ui
npm install
npm run dev
```

---

## 📋 What's Included

✅ **PostgreSQL Database** - Running in Docker container
✅ **Backend API** - FastAPI with endpoints documented in `/docs`
✅ **Frontend** - Next.js with API integration layer
✅ **Monitoring** - HealthCheck component shows backend status
✅ **Type Safety** - Full TypeScript support
✅ **Migrations** - Alembic for database schema management

---

## 🔗 API Integration

### Frontend API Service
All backend calls go through `src/services/api.ts`:

```typescript
import { apiService } from "@/services/api";

// Check backend health
const response = await apiService.getHealth();

// Get tickers
const tickers = await apiService.getTickers();

// Get filings for a symbol
const filings = await apiService.getFilings("AAPL");
```

### Custom Hook for Components
```typescript
import { useApi } from "@/hooks/useApi";
import { apiService } from "@/services/api";

export function MyComponent() {
  const { data, loading, error } = useApi(
    () => apiService.getTickers(),
    []
  );

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  return <div>{/* Use data */}</div>;
}
```

---

## 🗄️ Database

### PostgreSQL (Docker)
- Automatically starts with `docker-compose up`
- Connection: `postgresql://postgres:postgres@db:5432/signal_refinery`

### SQLite (Local Development)
- Automatically created at `backend/tickers.db` if PostgreSQL unavailable
- No configuration needed

### Migrations
```bash
# Create migration after schema changes
alembic revision --autogenerate -m "Description"

# Apply
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 📚 Documentation

- **[README.md](README.md)** - Full setup and overview
- **[DATABASE_SETUP.md](DATABASE_SETUP.md)** - Database configuration
- **[API_INTEGRATION.md](API_INTEGRATION.md)** - API endpoints and usage
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Complete change summary

---

## 🎯 Common Tasks

### Add New API Endpoint

1. **Create backend route** in `backend/routers/new_route.py`
2. **Add to main.py** `app.include_router(new_route.router)`
3. **Update frontend constants** in `ui/src/constants/index.ts`
4. **Add API method** in `ui/src/services/api.ts`
5. **Use in component** with `apiService` or `useApi` hook

### Check Database
```bash
# Docker PostgreSQL
docker-compose exec db psql -U postgres -d signal_refinery

# Local SQLite
sqlite3 backend/tickers.db
```

### View API Documentation
Open: **http://localhost:8000/docs**

### Reset Everything
```bash
docker-compose down -v  # Remove all volumes
docker-compose up       # Fresh start
```

---

## 🔍 Troubleshooting

**Backend not responding?**
- Check: `docker-compose ps` - all services running?
- Check logs: `docker-compose logs backend`

**Database connection error?**
- Wait a few seconds for database to be ready
- Check `DATABASE_URL` environment variable
- Try resetting: `docker-compose down -v && docker-compose up`

**Frontend can't reach backend?**
- Check `NEXT_PUBLIC_API_URL` environment variable
- Ensure backend is running on correct port
- Check browser DevTools Network tab for failed requests

---

## 📊 Project Structure

```
signal-refinery/
├── backend/              # Python FastAPI application
│   ├── main.py          # FastAPI app with CORS, health check
│   ├── database.py      # PostgreSQL/SQLite configuration
│   ├── requirements.txt  # Python dependencies
│   ├── routers/         # API endpoints
│   ├── services/        # Business logic
│   └── alembic/         # Database migrations
│
├── ui/                  # Next.js frontend application
│   ├── src/
│   │   ├── app/        # Pages and layout
│   │   ├── components/ # React components (+ new HealthCheck)
│   │   ├── services/   # API service layer
│   │   ├── hooks/      # Custom hooks (+ new useApi)
│   │   └── constants/  # App constants and API endpoints
│   └── package.json    # Node dependencies
│
├── docker-compose.yml   # Docker setup (PostgreSQL, backend, frontend)
└── *.md                # Documentation files
```

---

## 🎬 Next Steps

1. ✅ Start the application: `docker-compose up`
2. ✅ Verify health at: http://localhost:3000
3. ✅ Check API docs at: http://localhost:8000/docs
4. ✅ Create database migrations for your schema
5. ✅ Build API endpoints as needed
6. ✅ Implement frontend components using `apiService`

---

## 💡 Tips

- **Hot Reload:** Both backend and frontend automatically reload on file changes
- **API Docs:** Always available at `/docs` (Swagger) and `/redoc` (ReDoc)
- **Type Safety:** Frontend is fully typed with TypeScript for IDE autocomplete
- **Error Handling:** All API calls return standardized responses with error handling

---

Happy coding! 🎉
