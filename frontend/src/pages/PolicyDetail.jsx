import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import {
  getPolicy,
  getImpactAnalysis,
  predictRisk,
  getRecommendations,
  getExecutiveReport
} from '../services/api'
import ImpactChart from '../components/ImpactChart'
import RiskFactors from '../components/RiskFactors'
import RecommendationsList from '../components/RecommendationsList'
import ExecutiveReportView from '../components/ExecutiveReportView'
import './PolicyDetail.css'

function PolicyDetail() {
  const { id } = useParams()
  const [policy, setPolicy] = useState(null)
  const [impact, setImpact] = useState(null)
  const [risk, setRisk] = useState(null)
  const [recommendations, setRecommendations] = useState([])
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    loadPolicyData()
  }, [id])

  const loadPolicyData = async () => {
    try {
      setLoading(true)
      const [policyRes, impactRes, riskRes, recRes] = await Promise.all([
        getPolicy(id),
        getImpactAnalysis(id),
        predictRisk(id),
        getRecommendations(id)
      ])
      
      setPolicy(policyRes.data)
      setImpact(impactRes.data)
      setRisk(riskRes.data)
      setRecommendations(recRes.data)
      
      // Load report separately
      try {
        const reportRes = await getExecutiveReport(id)
        setReport(reportRes.data)
      } catch (err) {
        console.error('Failed to load report:', err)
      }
      
      setError(null)
    } catch (err) {
      setError('Failed to load policy data')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading policy details...</div>
  }

  if (error || !policy) {
    return (
      <div className="error">
        {error || 'Policy not found'}
        <Link to="/policies" className="btn btn-primary" style={{ marginTop: '10px', display: 'inline-block' }}>
          Back to Policies
        </Link>
      </div>
    )
  }

  return (
    <div className="policy-detail">
      <div className="container">
        <Link to="/policies" className="back-link">← Back to Policies</Link>
        
        <div className="policy-header">
          <div>
            <h1>{policy.name}</h1>
            <p className="policy-category">{policy.category}</p>
          </div>
          <span className={`status-badge status-${policy.status}`}>
            {policy.status}
          </span>
        </div>

        <div className="tabs">
          <button
            className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
          <button
            className={`tab ${activeTab === 'impact' ? 'active' : ''}`}
            onClick={() => setActiveTab('impact')}
          >
            Impact Analysis
          </button>
          <button
            className={`tab ${activeTab === 'risk' ? 'active' : ''}`}
            onClick={() => setActiveTab('risk')}
          >
            Risk Assessment
          </button>
          <button
            className={`tab ${activeTab === 'recommendations' ? 'active' : ''}`}
            onClick={() => setActiveTab('recommendations')}
          >
            Recommendations
          </button>
          <button
            className={`tab ${activeTab === 'report' ? 'active' : ''}`}
            onClick={() => setActiveTab('report')}
          >
            Executive Report
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'overview' && (
            <div className="overview-grid">
              <div className="card">
                <h2>Policy Information</h2>
                <div className="info-grid">
                  <div className="info-item">
                    <span className="info-label">Description:</span>
                    <p>{policy.description}</p>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Budget:</span>
                    <span className="info-value">${policy.budget.toLocaleString()}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Start Date:</span>
                    <span className="info-value">
                      {new Date(policy.start_date).toLocaleDateString()}
                    </span>
                  </div>
                  {policy.end_date && (
                    <div className="info-item">
                      <span className="info-label">End Date:</span>
                      <span className="info-value">
                        {new Date(policy.end_date).toLocaleDateString()}
                      </span>
                    </div>
                  )}
                </div>
              </div>

              {impact && (
                <div className="card">
                  <h2>Quick Stats</h2>
                  <div className="stats-grid">
                    <div className="stat-item">
                      <span className="stat-label">Impact Score</span>
                      <span className="stat-value">{impact.overall_impact_score}/100</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">ROI</span>
                      <span className="stat-value">{impact.roi.toFixed(1)}%</span>
                    </div>
                    {risk && (
                      <>
                        <div className="stat-item">
                          <span className="stat-label">Risk Score</span>
                          <span className="stat-value">{risk.risk_score}/100</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-label">Risk Level</span>
                          <span className={`stat-value risk-${risk.overall_risk_level}`}>
                            {risk.overall_risk_level.toUpperCase()}
                          </span>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'impact' && impact && (
            <div>
              <div className="card">
                <h2>Impact Analysis</h2>
                <div className="impact-summary">
                  <div className="impact-metric">
                    <span className="metric-label">Overall Impact Score</span>
                    <span className="metric-value">{impact.overall_impact_score}/100</span>
                  </div>
                  <div className="impact-metric">
                    <span className="metric-label">ROI</span>
                    <span className="metric-value">{impact.roi.toFixed(1)}%</span>
                  </div>
                </div>
              </div>

              <div className="card">
                <h2>Metrics Comparison</h2>
                <ImpactChart metrics={impact.metrics_comparison} trendData={impact.trend_data} />
              </div>

              <div className="card">
                <h2>Key Insights</h2>
                <ul className="insights-list">
                  {impact.key_insights.map((insight, idx) => (
                    <li key={idx}>{insight}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {activeTab === 'risk' && risk && (
            <div>
              <div className="card">
                <h2>Risk Assessment</h2>
                <div className="risk-summary">
                  <div className="risk-metric">
                    <span className="metric-label">Overall Risk Level</span>
                    <span className={`metric-value risk-${risk.overall_risk_level}`}>
                      {risk.overall_risk_level.toUpperCase()}
                    </span>
                  </div>
                  <div className="risk-metric">
                    <span className="metric-label">Risk Score</span>
                    <span className="metric-value">{risk.risk_score}/100</span>
                  </div>
                  <div className="risk-metric">
                    <span className="metric-label">Confidence</span>
                    <span className="metric-value">{(risk.confidence * 100).toFixed(1)}%</span>
                  </div>
                </div>
              </div>

              <RiskFactors factors={risk.risk_factors} />
            </div>
          )}

          {activeTab === 'recommendations' && (
            <RecommendationsList recommendations={recommendations} />
          )}

          {activeTab === 'report' && report && (
            <ExecutiveReportView report={report} />
          )}
        </div>
      </div>
    </div>
  )
}

export default PolicyDetail
