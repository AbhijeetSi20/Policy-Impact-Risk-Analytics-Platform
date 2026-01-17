import React from 'react'
import { Link } from 'react-router-dom'
import './Navbar.css'

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          📊 Policy Analytics Platform
        </Link>
        <div className="navbar-links">
          <Link to="/" className="navbar-link">Dashboard</Link>
          <Link to="/policies" className="navbar-link">Policies</Link>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
