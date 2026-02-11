import { useState, useEffect, useCallback } from "react";
import { apiService, type ApiResponse } from "@/services/api";

interface UseApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

/**
 * Custom hook for API requests
 * Handles loading, error, and data states
 */
export function useApi<T>(
  apiCall: () => Promise<ApiResponse<T>>,
  dependencies: any[] = []
): UseApiState<T> {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: true,
    error: null,
  });

  const fetchData = useCallback(async () => {
    setState({ data: null, loading: true, error: null });
    const response = await apiCall();

    if (response.data) {
      setState({ data: response.data, loading: false, error: null });
    } else {
      setState({
        data: null,
        loading: false,
        error: response.error || "Unknown error",
      });
    }
  }, [apiCall]);

  useEffect(() => {
    fetchData();
  }, dependencies);

  return state;
}
