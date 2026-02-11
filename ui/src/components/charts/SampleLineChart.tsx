'use client';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import colors from 'tailwindcss/colors';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface RevenueDataItem {
  symbol: string;
  filing_type: string;
  period_end: string;
  filing_date: string;
  revenue: number;
  revenue_label: string;
  unit: string;
}

interface MyChartProps {
  data: RevenueDataItem[];
}

export function MyChart({ data: revenueData }: MyChartProps) {
  const data = {
    labels: revenueData.map((item) => item.period_end),
    datasets: [
      {
        label: 'Revenue',
        data: revenueData.map((item) => item.revenue),
        backgroundColor: colors.blue[500]
      }
    ]
  };

  return <Bar className="bg-white" data={data} />;
}
