"use client";

import { useEffect, useState } from "react";
import { apiService, type HealthResponse } from "@/services/api";

interface HealthStatus {
  isHealthy: boolean;
  message: string;
  loading: boolean;
  error?: string;
}

export function HealthCheck() {
  const [health, setHealth] = useState<HealthStatus>({
    isHealthy: false,
    message: "Checking...",
    loading: true,
  });

  useEffect(() => {
    const checkHealth = async () => {
      const response = await apiService.getHealth();

      if (response.data) {
        setHealth({
          isHealthy: response.data.status === "healthy",
          message: response.data.message,
          loading: false,
        });
      } else {
        setHealth({
          isHealthy: false,
          message: "Backend is not responding",
          loading: false,
          error: response.error,
        });
      }
    };

    checkHealth();
    // Recheck health every 30 seconds
    const interval = setInterval(checkHealth, 30000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="rounded-lg border p-4">
      <div className="flex items-center gap-3">
        <div
          className={`h-3 w-3 rounded-full ${
            health.isHealthy ? "bg-green-500" : "bg-red-500"
          }`}
        />
        <div>
          <h3 className="font-semibold text-gray-900">Backend Status</h3>
          <p className="text-sm text-gray-600">{health.message}</p>
          {health.error && (
            <p className="text-sm text-red-600 mt-1">Error: {health.error}</p>
          )}
        </div>
      </div>
    </div>
  );
}
