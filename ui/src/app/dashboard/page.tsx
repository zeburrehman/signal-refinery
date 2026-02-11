import { MyChart } from '@/components/charts/SampleLineChart';

interface RevenueDataItem {
  symbol: string;
  filing_type: string;
  period_end: string;
  filing_date: string;
  revenue: number;
  revenue_label: string;
  unit: string;
}

interface RevenueResponse {
  symbol: string;
  filing_type: string;
  count: number;
  revenue_data: RevenueDataItem[];
}

async function fetchRevenueData(): Promise<RevenueDataItem[]> {
  const response = await fetch(
    'http://localhost:8000/revenue/AAPL?filing_type=10-Q'
  );
  if (!response.ok) {
    throw new Error('Failed to fetch revenue data');
  }
  const data: RevenueResponse = await response.json();
  return data.revenue_data;
}

export default async function Dashboard() {
  let revenueData: RevenueDataItem[] = [];
  let error: string | null = null;

  try {
    revenueData = await fetchRevenueData();
  } catch (err) {
    error = err instanceof Error ? err.message : 'An error occurred';
  }

  return (
    <div className="space-y-12">
      {error ? (
        <div className="p-4 text-red-500">Error: {error}</div>
      ) : (
        <MyChart data={revenueData} />
      )}
    </div>
  );
}
