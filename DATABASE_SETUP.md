# Database Setup and Migration Guide

## Overview

This project is configured to use PostgreSQL as the database (via Docker) with SQLAlchemy as the ORM. The setup supports both Docker-based PostgreSQL and SQLite for local development.

## Database Configuration

### Connection String

The application reads the database URL from the `DATABASE_URL` environment variable:

```
DATABASE_URL=postgresql://username:password@host:port/database_name
```

If not set, it defaults to SQLite (`sqlite:///./tickers.db`).

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/signal_refinery
```

Or use the `docker-compose.yml` environment variables:

```yaml
backend:
  environment:
    DATABASE_URL: postgresql://postgres:postgres@db:5432/signal_refinery
```

## Running with Docker

Start all services including PostgreSQL:

```bash
docker-compose up
```

The database will automatically initialize with tables created by SQLAlchemy on startup.

## Database Migrations with Alembic

Alembic is configured for managing database schema changes.

### Initialize Alembic (already done)

```bash
alembic init alembic
```

### Create a New Migration

After modifying models, create a migration:

```bash
alembic revision --autogenerate -m "Add new column"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Downgrade

```bash
alembic downgrade -1
```

### View Migration History

```bash
alembic current
alembic history
```

## Database Schema

The application uses three main tables:

### Filing10K
- Stores SEC 10-K (annual) filings
- Indexed by symbol, filing_date, and year
- Unique constraint on symbol + filing_date + url

### Filing10Q
- Stores SEC 10-Q (quarterly) filings
- Similar structure to Filing10K
- Includes quarter information

### FinancialData
- Stores extracted financial metrics from filings
- Includes statement type (Income Statement, Balance Sheet, etc.)
- Metric name, label, value, and unit

## Local Development

### Using SQLite (Default)

For local development without Docker:

```bash
cd backend
python -m uvicorn main:app --reload
```

SQLite database will be created at `backend/tickers.db`

### Using PostgreSQL Locally

Install PostgreSQL and create a database:

```bash
createdb signal_refinery
export DATABASE_URL="postgresql://postgres:password@localhost:5432/signal_refinery"
cd backend
python -m uvicorn main:app --reload
```

## Accessing the Database

### PostgreSQL in Docker

```bash
docker-compose exec db psql -U postgres -d signal_refinery
```

### SQLite

```bash
sqlite3 backend/tickers.db
```

## Troubleshooting

### Database Connection Issues

1. Ensure the database service is running: `docker-compose ps`
2. Check the DATABASE_URL environment variable
3. Verify the database exists and is accessible

### Migration Conflicts

If you encounter migration conflicts:

```bash
# Reset to a clean state (development only!)
alembic downgrade base
alembic upgrade head
```

### Fresh Database

To start with a clean database:

```bash
# With Docker
docker-compose down -v
docker-compose up

# With local PostgreSQL
dropdb signal_refinery
createdb signal_refinery
```

## Next Steps

1. Create migrations for any schema changes
2. Set up database backups for production
3. Configure connection pooling for production
4. Set up database monitoring and logging
