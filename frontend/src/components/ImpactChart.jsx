import React from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line, Bar } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
)

function ImpactChart({ metrics, trendData }) {
  // Comparison chart (Before vs After)
  const comparisonData = {
    labels: metrics.map(m => m.metric_name.replace(/_/g, ' ')),
    datasets: [
      {
        label: 'Before',
        data: metrics.map(m => m.before_value),
        backgroundColor: 'rgba(239, 68, 68, 0.5)',
        borderColor: 'rgb(239, 68, 68)',
        borderWidth: 2
      },
      {
        label: 'After',
        data: metrics.map(m => m.after_value),
        backgroundColor: 'rgba(16, 185, 129, 0.5)',
        borderColor: 'rgb(16, 185, 129)',
        borderWidth: 2
      }
    ]
  }

  const comparisonOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top'
      },
      title: {
        display: true,
        text: 'Before vs After Comparison'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }

  // Trend chart
  const trendChartData = {
    labels: Array.from({ length: 12 }, (_, i) => `Month ${i + 1}`),
    datasets: Object.entries(trendData).map(([metric, values], idx) => ({
      label: metric.replace(/_/g, ' '),
      data: values,
      borderColor: [
        'rgb(102, 126, 234)',
        'rgb(118, 75, 162)',
        'rgb(240, 147, 251)',
        'rgb(79, 172, 254)'
      ][idx % 4],
      backgroundColor: [
        'rgba(102, 126, 234, 0.1)',
        'rgba(118, 75, 162, 0.1)',
        'rgba(240, 147, 251, 0.1)',
        'rgba(79, 172, 254, 0.1)'
      ][idx % 4],
      tension: 0.4
    }))
  }

  const trendOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top'
      },
      title: {
        display: true,
        text: 'Trend Over Time'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
      <div style={{ height: '300px' }}>
        <Bar data={comparisonData} options={comparisonOptions} />
      </div>
      {Object.keys(trendData).length > 0 && (
        <div style={{ height: '300px' }}>
          <Line data={trendChartData} options={trendOptions} />
        </div>
      )}
    </div>
  )
}

export default ImpactChart
