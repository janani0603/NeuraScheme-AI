import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import './Navbar.css'

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [menuOpen, setMenuOpen] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)

  const isLanding = location.pathname === '/'

  const handleLogout = () => {
    logout()
    navigate('/')
    setMenuOpen(false)
    setMobileOpen(false)
  }

  const isActive = (path) => location.pathname === path

  return (
    <nav className={`navbar ${isLanding ? 'navbar-landing' : 'navbar-app'}`}>
      <div className="navbar-inner">
        <Link to="/" className="navbar-brand">
          <span className="brand-icon">🧠</span>
          <span className="brand-name">NeuraScheme <span>AI</span></span>
        </Link>

        {isLanding && (
          <ul className="navbar-links">
            <li><a href="#features">Features</a></li>
            <li><Link to="/explore" className={isActive('/explore') ? 'active' : ''}>Explore</Link></li>
            <li><a href="#about">About</a></li>
          </ul>
        )}

        <div className="navbar-actions">
          {isAuthenticated ? (
            <>
              <Link to="/notifications" className={`navbar-icon-btn ${isActive('/notifications') ? 'active' : ''}`} title="Notifications">🔔</Link>
              <div className="navbar-user" onClick={() => setMenuOpen(!menuOpen)}>
                <div className="user-avatar">{user?.name?.[0]?.toUpperCase() || 'U'}</div>
                <span className="user-name">{user?.name?.split(' ')[0]}</span>
                <span className={`chevron ${menuOpen ? 'open' : ''}`}>▾</span>
                {menuOpen && (
                  <div className="user-dropdown">
                    <Link to="/dashboard" onClick={() => setMenuOpen(false)}>📊 Dashboard</Link>
                    <Link to="/profile" onClick={() => setMenuOpen(false)}>👤 Profile</Link>
                    <Link to="/saved" onClick={() => setMenuOpen(false)}>❤️ Saved Schemes</Link>
                    <div className="dropdown-divider" />
                    <button onClick={handleLogout}>🚪 Logout</button>
                  </div>
                )}
              </div>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-ghost btn-sm">Login</Link>
              <Link to="/register" className="btn btn-primary btn-sm">Get Started</Link>
            </>
          )}
          <button className="hamburger" onClick={() => setMobileOpen(!mobileOpen)} aria-label="Menu">
            <span className={mobileOpen ? 'open' : ''} />
            <span className={mobileOpen ? 'open' : ''} />
            <span className={mobileOpen ? 'open' : ''} />
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="mobile-menu">
          {isLanding && (
            <>
              <a href="#features" onClick={() => setMobileOpen(false)}>Features</a>
              <a href="#about" onClick={() => setMobileOpen(false)}>About</a>
            </>
          )}
          <Link to="/explore" onClick={() => setMobileOpen(false)}>Explore Schemes</Link>
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" onClick={() => setMobileOpen(false)}>Dashboard</Link>
              <Link to="/profile" onClick={() => setMobileOpen(false)}>Profile</Link>
              <Link to="/saved" onClick={() => setMobileOpen(false)}>Saved Schemes</Link>
              <Link to="/assistant" onClick={() => setMobileOpen(false)}>AI Assistant</Link>
              <button onClick={handleLogout} className="mobile-logout">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" onClick={() => setMobileOpen(false)}>Login</Link>
              <Link to="/register" onClick={() => setMobileOpen(false)} className="mobile-cta">Get Started Free</Link>
            </>
          )}
        </div>
      )}
    </nav>
  )
}
