# Signal Refinery

A full-stack application for analyzing financial signals and SEC filings.

## Project Structure

```
signal-refinery/
├── backend/              # FastAPI Python backend
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── routers/         # API endpoints
│   ├── services/        # Business logic
│   └── ...
├── ui/                  # Next.js React frontend
│   ├── package.json
│   ├── Dockerfile
│   ├── src/
│   └── ...
├── docker-compose.yml   # Docker Compose configuration
└── README.md
```

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Or: Python 3.13+ and Node.js 20+

### Running with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd signal-refinery
   ```

2. **Start all services**
   ```bash
   docker-compose up
   ```

   This will start:
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **Database**: PostgreSQL on port 5432

3. **Stop services**
   ```bash
   docker-compose down
   ```

### Environment Variables

Create a `.env` file in the project root to override defaults:

```env
# Database Configuration
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_NAME=signal_refinery
DB_PORT=5432

# Backend Configuration
BACKEND_PORT=8000

# Frontend Configuration
FRONTEND_PORT=3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Running Locally (Development)

If you prefer to run services locally without Docker:

#### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

#### Frontend

```bash
cd ui
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Development Workflow

### Making Changes

**Backend changes:**
- Hot-reload is enabled by default in both Docker and local development
- Edit files in `backend/` and changes apply immediately

**Frontend changes:**
- Hot-reload is enabled in both Docker and local development
- Edit files in `ui/src/` and changes apply immediately

### Building for Production

```bash
# Build Docker images
docker-compose -f docker-compose.yml build

# Or locally
cd backend && pip install -r requirements.txt
cd ui && npm run build
```

## API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database

The application uses PostgreSQL (runs in Docker by default).

### Accessing the Database

```bash
# Using psql from your local machine
psql -h localhost -U postgres -d signal_refinery

# Or using Docker
docker-compose exec db psql -U postgres -d signal_refinery
```

## Troubleshooting

### Ports Already in Use

If ports 3000, 8000, or 5432 are already in use, modify the `.env` file:

```env
FRONTEND_PORT=3001
BACKEND_PORT=8001
DB_PORT=5433
```

### Database Connection Issues

Ensure the database service is healthy:

```bash
docker-compose ps
```

Wait a few seconds for the database to be ready. The backend has a health check that waits for the database.

### Clearing Docker Data

To start fresh with a clean database:

```bash
docker-compose down -v
docker-compose up
```

## Next Steps

- [ ] Configure database migrations
- [ ] Add authentication
- [ ] Set up CI/CD pipeline
- [ ] Deploy to production

## Support

For issues or questions, please check the project repository or create an issue.
