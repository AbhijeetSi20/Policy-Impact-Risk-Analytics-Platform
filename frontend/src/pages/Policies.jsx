import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getPolicies } from '../services/api'
import './Policies.css'

function Policies() {
  const [policies, setPolicies] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    loadPolicies()
  }, [])

  const loadPolicies = async () => {
    try {
      setLoading(true)
      const response = await getPolicies()
      setPolicies(response.data)
      setError(null)
    } catch (err) {
      setError('Failed to load policies')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const filteredPolicies = filter === 'all' 
    ? policies 
    : policies.filter(p => p.status === filter)

  const getStatusColor = (status) => {
    const colors = {
      draft: '#6b7280',
      active: '#10b981',
      completed: '#3b82f6',
      archived: '#9ca3af'
    }
    return colors[status] || '#6b7280'
  }

  if (loading) {
    return <div className="loading">Loading policies...</div>
  }

  if (error) {
    return <div className="error">{error}</div>
  }

  return (
    <div className="policies-page">
      <div className="container">
        <div className="page-header">
          <h1>Policies</h1>
          <div className="filters">
            <button
              className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
              onClick={() => setFilter('all')}
            >
              All
            </button>
            <button
              className={`filter-btn ${filter === 'active' ? 'active' : ''}`}
              onClick={() => setFilter('active')}
            >
              Active
            </button>
            <button
              className={`filter-btn ${filter === 'completed' ? 'active' : ''}`}
              onClick={() => setFilter('completed')}
            >
              Completed
            </button>
            <button
              className={`filter-btn ${filter === 'draft' ? 'active' : ''}`}
              onClick={() => setFilter('draft')}
            >
              Draft
            </button>
          </div>
        </div>

        <div className="policies-grid">
          {filteredPolicies.map(policy => (
            <Link
              key={policy.id}
              to={`/policies/${policy.id}`}
              className="policy-card"
            >
              <div className="policy-header">
                <h3>{policy.name}</h3>
                <span
                  className="status-badge"
                  style={{ backgroundColor: getStatusColor(policy.status) }}
                >
                  {policy.status}
                </span>
              </div>
              <p className="policy-description">{policy.description}</p>
              <div className="policy-meta">
                <div className="meta-item">
                  <span className="meta-label">Category:</span>
                  <span className="meta-value">{policy.category}</span>
                </div>
                <div className="meta-item">
                  <span className="meta-label">Budget:</span>
                  <span className="meta-value">
                    ${(policy.budget / 1000).toFixed(0)}K
                  </span>
                </div>
                <div className="meta-item">
                  <span className="meta-label">Start Date:</span>
                  <span className="meta-value">
                    {new Date(policy.start_date).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>

        {filteredPolicies.length === 0 && (
          <div className="empty-state">
            <p>No policies found with the selected filter.</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Policies
