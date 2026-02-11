# Local Development Setup (Without Docker)

## Overview

Run both backend and frontend locally for fast development iteration without Docker.

---

## Prerequisites

- **Python 3.13+** installed
- **Node.js 20+** installed
- **npm** package manager

Check your versions:
```bash
python --version
node --version
npm --version
```

---

## Backend Setup

### Step 1: Navigate to backend directory
```bash
cd backend
```

### Step 2: Create virtual environment (recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

**Note:** If you encounter the `pg_config` error, the requirements have been updated to use pre-built wheels. Just run the install again.

### Step 4: Start the backend server
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Will watch for changes in these directories: ['...backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

**Backend is running at:** http://localhost:8000

---

## Frontend Setup

### Step 1: Open new terminal and navigate to UI directory
```bash
cd ui
```

### Step 2: Install dependencies
```bash
npm install
```

### Step 3: Start the development server
```bash
npm run dev
```

You should see:
```
  ▲ Next.js 16.1.6
  - Local:        http://localhost:3000
  - Environments: .env.local

✓ Ready in 2.5s
```

**Frontend is running at:** http://localhost:3000

---

## Verification

### 1. Check Backend Health
Open in browser or terminal:
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

### 2. Check Frontend
Open in browser: http://localhost:3000

You should see:
- ✅ Hero section with welcome message
- ✅ **Backend Status** card (green indicator = healthy)
- ✅ Features section

### 3. Check API Documentation
Open: http://localhost:8000/docs

Interactive API documentation with all endpoints.

---

## Database Setup

### Using SQLite (Default - No Configuration Needed)

SQLite database will be automatically created at `backend/tickers.db`

No additional setup required!

### Using PostgreSQL (Optional)

If you want to test with PostgreSQL locally:

#### 1. Install PostgreSQL
- Download from: https://www.postgresql.org/download/
- Install and remember your password

#### 2. Create database
```bash
createdb signal_refinery
```

#### 3. Set environment variable
```bash
# On Windows (Command Prompt):
set DATABASE_URL=postgresql://postgres:your_password@localhost:5432/signal_refinery

# On Windows (PowerShell):
$env:DATABASE_URL="postgresql://postgres:your_password@localhost:5432/signal_refinery"

# On macOS/Linux:
export DATABASE_URL="postgresql://postgres:your_password@localhost:5432/signal_refinery"
```

#### 4. Restart backend
The backend will now use PostgreSQL instead of SQLite.

---

## File Structure

```
signal-refinery/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── requirements.txt      # Python dependencies
│   ├── routers/             # API endpoints
│   ├── services/            # Business logic
│   ├── tickers.db           # SQLite database (auto-created)
│   └── venv/                # Virtual environment (created by you)
│
└── ui/
    ├── package.json         # Node dependencies
    ├── src/
    │   ├── app/            # Pages
    │   ├── components/     # React components
    │   ├── services/       # API service layer
    │   ├── hooks/          # Custom hooks
    │   └── constants/      # App constants
    └── node_modules/       # Node packages (created by npm install)
```

---

## Development Workflow

### Making Changes

**Backend:**
- Edit files in `backend/`
- Changes auto-reload (watch enabled)
- No need to restart server

**Frontend:**
- Edit files in `ui/src/`
- Changes auto-reload (hot reload)
- Browser updates automatically

### Testing Changes

1. Make a change to either backend or frontend
2. Backend: reload happens automatically
3. Frontend: browser refreshes automatically
4. Test your changes in browser at http://localhost:3000

---

## Common Issues

### Issue: Port already in use

**Backend (port 8000):**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F

# Or use different port
python -m uvicorn main:app --reload --port 8001
```

**Frontend (port 3000):**
```bash
# Find process using port 3000
netstat -ano | findstr :3000

# Kill process
taskkill /PID <PID> /F

# Or use different port
npm run dev -- --port 3001
```

### Issue: Virtual environment not activated

You should see `(venv)` at the start of your terminal line.

If not, activate it:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Issue: npm dependencies not installed

Run:
```bash
cd ui
npm install
```

### Issue: SQLite database locked

Delete and recreate:
```bash
rm backend/tickers.db
# Restart backend to recreate
```

---

## Environment Variables

Create `.env` files if you need custom settings:

### backend/.env
```env
DATABASE_URL=postgresql://user:password@localhost:5432/signal_refinery
PYTHONUNBUFFERED=1
```

### ui/.env.local
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Next Steps

1. ✅ Backend running on http://localhost:8000
2. ✅ Frontend running on http://localhost:3000
3. ✅ Backend health check passing (green indicator on home page)
4. Create your first API endpoint
5. Build a frontend component using the API
6. Test database migrations with Alembic

---

## Debugging

### Backend Logs

Terminal where backend is running shows all logs:
```
INFO:     127.0.0.1:50000 - "GET /api/health HTTP/1.1" 200 OK
```

### Frontend Logs

Terminal where frontend is running shows all logs:
```
  ▲ GET / 200 in 234ms (v16.1.6)
```

Browser Console (F12 → Console):
```javascript
// API calls are logged here
// Network tab shows all requests
```

### Database Logs

For SQLite:
```bash
# Just open the database file
sqlite3 backend/tickers.db
.tables
```

---

## Useful Commands

```bash
# Backend
python -m uvicorn main:app --reload          # Run with hot reload
python -m uvicorn main:app                   # Run without reload
alembic revision --autogenerate -m "Add field"  # Create migration
alembic upgrade head                         # Apply migrations

# Frontend
npm run dev                                  # Start development server
npm run build                                # Create production build
npm run lint                                 # Check code style
npm run type-check                           # TypeScript check

# Database
sqlite3 backend/tickers.db                   # Open SQLite database
psql -d signal_refinery                      # Open PostgreSQL (if installed)
```

---

## Performance Tips

1. **Use virtual environment** - Isolates dependencies
2. **Keep terminals separate** - One for backend, one for frontend
3. **Check system resources** - If slow, close other apps
4. **Clear npm cache** - `npm cache clean --force` if issues
5. **Restart if stuck** - Kill both servers and restart

---

## Ready to Code!

You now have a fully functional local development environment.

Start with:
1. Backend: `python -m uvicorn main:app --reload`
2. Frontend: `npm run dev`
3. Visit: http://localhost:3000
4. Code! 🚀
