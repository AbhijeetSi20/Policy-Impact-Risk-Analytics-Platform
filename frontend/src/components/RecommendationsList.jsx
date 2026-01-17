import React from 'react'
import './RecommendationsList.css'

function RecommendationsList({ recommendations }) {
  const getPriorityColor = (priority) => {
    const colors = {
      high: '#ef4444',
      medium: '#f59e0b',
      low: '#10b981'
    }
    return colors[priority] || '#6b7280'
  }

  const getCategoryIcon = (category) => {
    const icons = {
      budget: '💰',
      timeline: '⏰',
      strategy: '🎯',
      risk_mitigation: '🛡️'
    }
    return icons[category] || '📋'
  }

  return (
    <div className="recommendations">
      <div className="card">
        <h2>Recommendations</h2>
        <div className="recommendations-list">
          {recommendations.map((rec, idx) => (
            <div key={idx} className="recommendation-card">
              <div className="recommendation-header">
                <div className="recommendation-title-section">
                  <span className="category-icon">
                    {getCategoryIcon(rec.category)}
                  </span>
                  <h3>{rec.title}</h3>
                </div>
                <span
                  className="priority-badge"
                  style={{ backgroundColor: getPriorityColor(rec.priority) }}
                >
                  {rec.priority.toUpperCase()}
                </span>
              </div>
              <p className="recommendation-description">{rec.description}</p>
              <div className="recommendation-meta">
                <div className="meta-item">
                  <strong>Expected Impact:</strong> {rec.expected_impact}
                </div>
                <div className="meta-item">
                  <strong>Implementation Effort:</strong> {rec.implementation_effort}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default RecommendationsList
