import React from 'react'
import './RiskFactors.css'

function RiskFactors({ factors }) {
  const getRiskColor = (score) => {
    if (score >= 70) return '#ef4444'
    if (score >= 50) return '#f59e0b'
    return '#10b981'
  }

  return (
    <div className="risk-factors">
      <h2>Risk Factors</h2>
      <div className="factors-list">
        {factors.map((factor, idx) => (
          <div key={idx} className="risk-factor-card">
            <div className="factor-header">
              <h3>{factor.factor_name}</h3>
              <div
                className="risk-score-badge"
                style={{ backgroundColor: getRiskColor(factor.risk_score) }}
              >
                {factor.risk_score}/100
              </div>
            </div>
            <p className="factor-description">{factor.description}</p>
            {factor.mitigation_strategy && (
              <div className="mitigation-strategy">
                <strong>Mitigation:</strong> {factor.mitigation_strategy}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default RiskFactors
