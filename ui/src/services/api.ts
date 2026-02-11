import { API_ENDPOINTS } from "@/constants";

/**
 * API Service Layer
 * Centralized API communication for all backend endpoints
 */

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface HealthResponse {
  status: string;
  message: string;
}

class ApiService {
  private async request<T>(
    url: string,
    options?: RequestInit
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(url, {
        headers: {
          "Content-Type": "application/json",
          ...options?.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Unknown error occurred";
      console.error("API Error:", errorMessage);
      return { error: errorMessage };
    }
  }

  /**
   * Health Check Endpoints
   */
  async getHealth(): Promise<ApiResponse<HealthResponse>> {
    return this.request<HealthResponse>(API_ENDPOINTS.HEALTH);
  }

  /**
   * Ticker Endpoints
   */
  async getTickers(): Promise<ApiResponse<any>> {
    return this.request(API_ENDPOINTS.TICKERS.LIST);
  }

  async getTicker(symbol: string): Promise<ApiResponse<any>> {
    return this.request(API_ENDPOINTS.TICKERS.GET(symbol));
  }

  async analyzeTicker(symbol: string): Promise<ApiResponse<any>> {
    return this.request(API_ENDPOINTS.TICKERS.ANALYZE(symbol));
  }

  async addTicker(tickerData: any): Promise<ApiResponse<any>> {
    return this.request(API_ENDPOINTS.TICKERS.LIST, {
      method: "POST",
      body: JSON.stringify(tickerData),
    });
  }

  /**
   * Filing Endpoints
   */
  async getFilings(symbol: string): Promise<ApiResponse<any>> {
    return this.request(API_ENDPOINTS.FILINGS.LIST(symbol));
  }

  async fetchFilings(symbol: string): Promise<ApiResponse<any>> {
    return this.request(API_ENDPOINTS.FILINGS.FETCH(symbol), {
      method: "POST",
    });
  }

  /**
   * Financial Data Endpoints
   */
  async getFinancials(symbol: string): Promise<ApiResponse<any>> {
    return this.request(API_ENDPOINTS.FINANCIALS.LIST(symbol));
  }
}

// Export singleton instance
export const apiService = new ApiService();
