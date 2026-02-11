# Testing Guide

## Verifying the Complete Setup

This guide helps you verify all three integration steps are working correctly.

---

## 1. Health Check - Backend Status

### Test via Frontend UI
1. Start the application: `docker-compose up`
2. Open http://localhost:3000 in your browser
3. Look for the **Backend Status** card with a colored indicator dot:
   - **Green dot** = Backend is healthy ✅
   - **Red dot** = Backend is not responding ❌

### Test via API
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Signal Refinery API is running"
}
```

---

## 2. Database Connection - PostgreSQL Integration

### Verify Database is Running
```bash
docker-compose ps
```

You should see three containers:
```
signal-refinery-db        ✓ postgres:16-alpine
signal-refinery-backend   ✓ python app
signal-refinery-frontend  ✓ next.js app
```

### Connect to Database
```bash
# Using Docker
docker-compose exec db psql -U postgres -d signal_refinery

# Or if PostgreSQL is installed locally
psql -h localhost -U postgres -d signal_refinery -p 5432
```

### List Tables
```sql
\dt
```

You should see:
```
filings_10k
filings_10q
financial_data
```

---

## 3. API Integration - Frontend to Backend

### Check Network Communication

1. Open http://localhost:3000 in browser
2. Open Developer Tools (F12)
3. Go to **Network** tab
4. Refresh the page
5. Look for requests to:
   - `GET http://localhost:8000/api/health` → Status 200 ✅

### Test Tickers Endpoint

**Via Browser Console:**
```javascript
// In DevTools Console, paste this:
fetch('http://localhost:8000/tickers')
  .then(r => r.json())
  .then(d => console.log(d))
  .catch(e => console.error(e))
```

**Via cURL:**
```bash
curl http://localhost:8000/tickers
```

---

## 4. Database Migrations - Alembic Setup

### Verify Alembic Structure
```bash
ls -la backend/alembic/
# Should show: env.py, script.py.mako, versions/
```

### Check Current Migration State
```bash
cd backend
alembic current
# Should show the current revision
```

### View Migration History
```bash
alembic history
# Lists all applied migrations
```

---

## 5. Frontend API Service Layer

### Test API Service Directly

Create a test file `test-api.js`:
```javascript
import { apiService } from '@/services/api';

async function test() {
  // Test health check
  const health = await apiService.getHealth();
  console.log('Health:', health);

  // Test tickers
  const tickers = await apiService.getTickers();
  console.log('Tickers:', tickers);
}

test();
```

Or use the browser console:
```javascript
// In Next.js app console:
import { apiService } from '@/services/api';
apiService.getHealth().then(r => console.log(r));
```

---

## 6. TypeScript Type Safety

### Verify Types are Working

The API service is fully typed. Your IDE should show autocomplete:

```typescript
// Type checking in editor
apiService.getTickers() // Shows return type in IDE
apiService.getTicker('AAPL') // Shows parameter hints
```

Open `ui/src/services/api.ts` and verify:
- ✅ Interface definitions for responses
- ✅ Method signatures with proper types
- ✅ Error handling with string unions

---

## 7. Hot Reload

### Backend Hot Reload
```bash
# Terminal 1: Run backend
cd backend
python -m uvicorn main:app --reload

# Terminal 2: Edit a file in backend/
# You should see "Reloading" message in Terminal 1
```

### Frontend Hot Reload
```bash
# Terminal 1: Run frontend
cd ui
npm run dev

# Terminal 2: Edit ui/src/app/page.tsx
# Browser should refresh automatically
```

---

## 8. Docker Compose Full Test

### Comprehensive Test Suite

```bash
#!/bin/bash
set -e

echo "🧪 Starting comprehensive tests..."

# 1. Check containers
echo "✓ Checking Docker containers..."
docker-compose ps

# 2. Health check
echo "✓ Testing API health endpoint..."
curl -s http://localhost:8000/api/health | json_pp

# 3. Database connection
echo "✓ Testing database connection..."
docker-compose exec -T db psql -U postgres -d signal_refinery -c "SELECT 1"

# 4. Frontend availability
echo "✓ Testing frontend availability..."
curl -s http://localhost:3000 | head -20

# 5. API Documentation
echo "✓ Testing API documentation..."
curl -s http://localhost:8000/docs | head -20

echo "✅ All tests passed!"
```

Save as `test.sh` and run:
```bash
chmod +x test.sh
./test.sh
```

---

## 9. Common Issues and Fixes

### Issue: Backend returning 503/Connection Error

**Solution:**
```bash
# Wait for database to be ready
docker-compose ps  # Check db health

# Or restart completely
docker-compose down
docker-compose up
```

### Issue: Frontend can't reach backend (CORS error)

**Solution:**
1. Verify `NEXT_PUBLIC_API_URL` is correct
2. Check if backend is actually running: `curl http://localhost:8000/health`
3. Clear browser cache and try again

### Issue: Database port already in use

**Solution:**
```bash
# Use different port in docker-compose
export DB_PORT=5433
docker-compose up
```

### Issue: Migrations fail

**Solution:**
```bash
# Reset to clean state (development only!)
docker-compose down -v
docker-compose up
```

---

## 10. Performance Testing

### Load Testing API

```bash
# Using Apache Bench
ab -n 100 -c 10 http://localhost:8000/api/health

# Expected: All requests should succeed with 200 status
```

### Database Connection Pool

The backend is configured with:
- `pool_pre_ping=True` - Validates connections before use
- `pool_recycle=3600` - Recycles connections after 1 hour

This is visible in `backend/database.py`.

---

## 11. Monitoring

### Backend Logs
```bash
docker-compose logs -f backend
```

### Frontend Logs
```bash
docker-compose logs -f frontend
```

### Database Activity
```bash
docker-compose exec db psql -U postgres -d signal_refinery -c "\conninfo"
```

---

## 12. Production Readiness Checklist

Before deploying to production, verify:

- [ ] Environment variables are properly set
- [ ] CORS is configured for specific domains
- [ ] Database backups are configured
- [ ] Logging and monitoring are set up
- [ ] Error handling covers edge cases
- [ ] API rate limiting is implemented
- [ ] Authentication is implemented
- [ ] SSL/TLS certificates are installed
- [ ] Database migrations are tested
- [ ] All endpoints are documented

---

## Success Indicators

✅ **Step 1 Complete:** PostgreSQL container running with tables created
✅ **Step 2 Complete:** API endpoints respond with correct data
✅ **Step 3 Complete:** Frontend displays health check with backend status

If you see all three green indicators, you're ready to go! 🎉

---

## Next Steps

1. Create your first database migration
2. Add new API endpoints
3. Build frontend features using the API service layer
4. Deploy to production
5. Set up monitoring and logging
