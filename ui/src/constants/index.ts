/**
 * Application constants
 */

export const APP_NAME = "Signal Refinery UI";
export const APP_VERSION = "0.1.0";

export const ROUTES = {
  HOME: "/",
  DASHBOARD: "/dashboard",
  SETTINGS: "/settings",
} as const;

// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const API_ENDPOINTS = {
  BASE_URL: API_BASE_URL,
  HEALTH: `${API_BASE_URL}/api/health`,
  TICKERS: {
    LIST: `${API_BASE_URL}/tickers`,
    GET: (symbol: string) => `${API_BASE_URL}/tickers/${symbol}`,
    ANALYZE: (symbol: string) => `${API_BASE_URL}/tickers/${symbol}/analyze`,
  },
  FILINGS: {
    LIST: (symbol: string) => `${API_BASE_URL}/filings/${symbol}`,
    FETCH: (symbol: string) => `${API_BASE_URL}/filings/${symbol}`,
  },
  FINANCIALS: {
    LIST: (symbol: string) => `${API_BASE_URL}/financials/${symbol}`,
  },
} as const;
