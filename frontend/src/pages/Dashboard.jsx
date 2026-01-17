import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getDashboardMetrics, getPolicies } from '../services/api'
import MetricCard from '../components/MetricCard'
import PolicyChart from '../components/PolicyChart'
import RecentActivities from '../components/RecentActivities'
import './Dashboard.css'

function Dashboard() {
  const [metrics, setMetrics] = useState(null)
  const [policies, setPolicies] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [metricsRes, policiesRes] = await Promise.all([
        getDashboardMetrics(),
        getPolicies()
      ])
      setMetrics(metricsRes.data)
      setPolicies(policiesRes.data)
      setError(null)
    } catch (err) {
      setError('Failed to load dashboard data')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading dashboard...</div>
  }

  if (error) {
    return <div className="error">{error}</div>
  }

  return (
    <div className="dashboard">
      <div className="container">
        <h1 className="dashboard-title">Policy Analytics Dashboard</h1>
        
        <div className="metrics-grid">
          <MetricCard
            title="Total Policies"
            value={metrics.total_policies}
            icon="📋"
            color="#3b82f6"
          />
          <MetricCard
            title="Active Policies"
            value={metrics.active_policies}
            icon="✅"
            color="#10b981"
          />
          <MetricCard
            title="Total Budget"
            value={`$${(metrics.total_budget / 1000000).toFixed(2)}M`}
            icon="💰"
            color="#f59e0b"
          />
          <MetricCard
            title="Average ROI"
            value={`${metrics.average_roi.toFixed(1)}%`}
            icon="📈"
            color="#8b5cf6"
          />
          <MetricCard
            title="High Risk Policies"
            value={metrics.high_risk_policies}
            icon="⚠️"
            color="#ef4444"
          />
        </div>

        <div className="dashboard-grid">
          <div className="card">
            <h2>Policies by Status</h2>
            <PolicyChart
              data={metrics.policies_by_status}
              type="doughnut"
            />
          </div>

          <div className="card">
            <h2>Policies by Category</h2>
            <PolicyChart
              data={metrics.policies_by_category}
              type="bar"
            />
          </div>
        </div>

        <div className="card">
          <div className="section-header">
            <h2>Recent Activities</h2>
            <Link to="/policies" className="btn btn-primary">
              View All Policies
            </Link>
          </div>
          <RecentActivities activities={metrics.recent_activities} />
        </div>
      </div>
    </div>
  )
}

export default Dashboard
