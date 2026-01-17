import React from 'react'
import { Link } from 'react-router-dom'
import { format } from 'date-fns'
import './RecentActivities.css'

function RecentActivities({ activities }) {
  return (
    <div className="activities-list">
      {activities.map((activity, idx) => (
        <Link
          key={idx}
          to={`/policies/${activity.policy_id}`}
          className="activity-item"
        >
          <div className="activity-icon">📋</div>
          <div className="activity-content">
            <div className="activity-title">{activity.policy_name}</div>
            <div className="activity-meta">
              <span className="activity-action">{activity.action}</span>
              <span className="activity-time">
                {format(new Date(activity.timestamp), 'MMM d, yyyy')}
              </span>
            </div>
          </div>
        </Link>
      ))}
    </div>
  )
}

export default RecentActivities
