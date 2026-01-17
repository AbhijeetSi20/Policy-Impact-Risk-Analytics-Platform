import React from 'react'
import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Doughnut, Bar } from 'react-chartjs-2'

ChartJS.register(
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

function PolicyChart({ data, type = 'doughnut' }) {
  const labels = Object.keys(data)
  const values = Object.values(data)

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Count',
        data: values,
        backgroundColor: [
          '#667eea',
          '#764ba2',
          '#f093fb',
          '#4facfe',
          '#00f2fe',
          '#43e97b',
          '#fa709a',
          '#fee140'
        ],
        borderWidth: 2,
        borderColor: '#fff'
      }
    ]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'bottom'
      }
    }
  }

  return (
    <div style={{ height: '300px', position: 'relative' }}>
      {type === 'doughnut' ? (
        <Doughnut data={chartData} options={options} />
      ) : (
        <Bar data={chartData} options={options} />
      )}
    </div>
  )
}

export default PolicyChart
