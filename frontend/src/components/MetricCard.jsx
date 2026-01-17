import React from 'react'
import './MetricCard.css'

function MetricCard({ title, value, icon, color }) {
  return (
    <div className="metric-card" style={{ borderTopColor: color }}>
      <div className="metric-icon">{icon}</div>
      <div className="metric-content">
        <div className="metric-title">{title}</div>
        <div className="metric-value" style={{ color }}>
          {value}
        </div>
      </div>
    </div>
  )
}

export default MetricCard
