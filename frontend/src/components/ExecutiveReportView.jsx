import React from 'react'
import { format } from 'date-fns'
import './ExecutiveReportView.css'

function ExecutiveReportView({ report }) {
  return (
    <div className="executive-report">
      <div className="card">
        <div className="report-header">
          <h1>Executive Report</h1>
          <div className="report-meta">
            <span>Generated: {format(new Date(report.generated_at), 'PPpp')}</span>
          </div>
        </div>

        <div className="report-section">
          <h2>Executive Summary</h2>
          <p className="executive-summary">{report.executive_summary}</p>
        </div>

        <div className="report-section">
          <h2>Key Metrics</h2>
          <div className="key-metrics-grid">
            {Object.entries(report.key_metrics).map(([key, value]) => (
              <div key={key} className="key-metric-item">
                <span className="key-metric-label">
                  {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </span>
                <span className="key-metric-value">
                  {typeof value === 'number' ? value.toFixed(2) : value}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="report-section">
          <h2>Impact Analysis Summary</h2>
          <div className="summary-grid">
            <div className="summary-item">
              <span className="summary-label">Impact Score</span>
              <span className="summary-value">
                {report.impact_analysis.overall_impact_score}/100
              </span>
            </div>
            <div className="summary-item">
              <span className="summary-label">ROI</span>
              <span className="summary-value">
                {report.impact_analysis.roi.toFixed(1)}%
              </span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Metrics Tracked</span>
              <span className="summary-value">
                {report.impact_analysis.metrics_comparison.length}
              </span>
            </div>
          </div>
        </div>

        <div className="report-section">
          <h2>Risk Assessment Summary</h2>
          <div className="summary-grid">
            <div className="summary-item">
              <span className="summary-label">Risk Level</span>
              <span className={`summary-value risk-${report.risk_assessment.overall_risk_level}`}>
                {report.risk_assessment.overall_risk_level.toUpperCase()}
              </span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Risk Score</span>
              <span className="summary-value">
                {report.risk_assessment.risk_score}/100
              </span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Confidence</span>
              <span className="summary-value">
                {(report.risk_assessment.confidence * 100).toFixed(1)}%
              </span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Risk Factors</span>
              <span className="summary-value">
                {report.risk_assessment.risk_factors.length}
              </span>
            </div>
          </div>
        </div>

        <div className="report-section">
          <h2>Recommendations Summary</h2>
          <p className="recommendations-count">
            {report.recommendations.length} recommendation(s) provided
          </p>
          <div className="recommendations-preview">
            {report.recommendations.slice(0, 3).map((rec, idx) => (
              <div key={idx} className="recommendation-preview-item">
                <strong>{rec.title}</strong> - {rec.description.substring(0, 100)}...
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ExecutiveReportView
