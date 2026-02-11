# API Integration Guide

## Overview

This guide explains how the frontend and backend are integrated via REST APIs.

## Backend API Endpoints

### Health Check

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "message": "Signal Refinery API is running"
}
```

### Tickers

**List Tickers**
- `GET /tickers` - Get all tickers

**Add Ticker**
- `POST /tickers` - Add a new ticker
- Body: `{"symbol": "AAPL"}`

**Get Ticker**
- `GET /tickers/{symbol}` - Get specific ticker

**Analyze Ticker**
- `GET /tickers/{symbol}/analyze` - Get analysis for a ticker

### Filings

**Get Filings**
- `GET /filings/{symbol}` - Get all filings for a symbol

**Fetch Filings**
- `POST /filings/{symbol}` - Fetch and store new filings from SEC

### Financials

**Get Financial Data**
- `GET /financials/{symbol}` - Get financial metrics for a symbol

## Frontend API Integration

### API Service Layer

The frontend uses a centralized API service (`src/services/api.ts`) for all backend communication.

**Usage Example:**
```typescript
import { apiService } from "@/services/api";

// Get tickers
const response = await apiService.getTickers();
if (response.data) {
  console.log("Tickers:", response.data);
} else {
  console.error("Error:", response.error);
}
```

### Available Methods

#### Health
- `getHealth()` - Check backend health

#### Tickers
- `getTickers()` - Get all tickers
- `getTicker(symbol)` - Get specific ticker
- `analyzeTicker(symbol)` - Analyze ticker
- `addTicker(tickerData)` - Add new ticker

#### Filings
- `getFilings(symbol)` - Get filings
- `fetchFilings(symbol)` - Fetch new filings

#### Financials
- `getFinancials(symbol)` - Get financial data

### Using the useApi Hook

For React components that need to fetch data:

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

  return (
    <div>
      {data?.map((ticker: any) => (
        <div key={ticker.symbol}>{ticker.symbol}</div>
      ))}
    </div>
  );
}
```

### Creating New API Endpoints

1. **Backend**: Add endpoint in `backend/routers/`
2. **Frontend Constants**: Update `ui/src/constants/index.ts` with the new endpoint URL
3. **API Service**: Add method in `ui/src/services/api.ts`
4. **Component**: Use in React components via `apiService` or `useApi` hook

## Error Handling

All API responses follow a standard format:

```typescript
interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}
```

**Example:**
```typescript
const response = await apiService.getTickers();

if (response.data) {
  // Success - use response.data
} else if (response.error) {
  // Error - handle response.error
  console.error(response.error);
}
```

## CORS Configuration

The backend is configured with CORS enabled for all origins in development:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For Production**: Configure `allow_origins` with specific frontend URL(s).

## API Documentation

Interactive API documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Environment Variables

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL (defaults to `http://localhost:8000`)

### Backend
- `DATABASE_URL` - PostgreSQL connection string
- `PYTHONUNBUFFERED` - Set to 1 for real-time logs

## Testing API Endpoints

### Using cURL

```bash
# Health check
curl http://localhost:8000/api/health

# Get tickers
curl http://localhost:8000/tickers

# Add ticker
curl -X POST http://localhost:8000/tickers \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}'
```

### Using Postman

1. Import the API endpoints
2. Configure environment variables
3. Test each endpoint

## Rate Limiting

No rate limiting is currently configured. For production, consider adding rate limiting middleware.

## Authentication

Currently, no authentication is implemented. Add authentication middleware as needed for sensitive endpoints.

## Next Steps

1. Implement proper error responses
2. Add request/response validation
3. Add authentication and authorization
4. Implement rate limiting
5. Add API versioning
6. Set up API monitoring and logging
