import { useState, useEffect, useRef } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { Brain, Bell, LayoutDashboard, User, Bookmark, LogOut } from 'lucide-react'
import api from '../../services/api'
import './Navbar.css'

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [menuOpen, setMenuOpen] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)

  const isLanding = location.pathname === '/'
  const [unreadCount, setUnreadCount] = useState(0)
  const pollRef = useRef(null)

  useEffect(() => {
    if (!isAuthenticated) return
    const fetchCount = () =>
      api.get('/notifications/unread-count')
        .then(r => setUnreadCount(r.data.unread_count))
        .catch(() => {})
    fetchCount()
    pollRef.current = setInterval(fetchCount, 30000)
    return () => clearInterval(pollRef.current)
  }, [isAuthenticated])

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
          <div className="brand-icon"><Brain size={18} /></div>
          <span className="brand-name">NeuraScheme <span>AI</span></span>
        </Link>

        {isLanding && (
          <ul className="navbar-links">
            <li><a href="#features">Features</a></li>
            <li><Link to="/explore" className={isActive('/explore') ? 'active' : ''}>Explore</Link></li>
            <li><a href="#about">About</a></li>
          </ul>
        )}

        {isAuthenticated && !isLanding && (
          <ul className="navbar-links">
            <li><Link to="/dashboard" className={isActive('/dashboard') ? 'active' : ''}>Dashboard</Link></li>
            <li><Link to="/explore" className={isActive('/explore') ? 'active' : ''}>Explore</Link></li>
            <li><Link to="/eligibility" className={isActive('/eligibility') ? 'active' : ''}>Eligibility</Link></li>
            <li><Link to="/assistant" className={isActive('/assistant') ? 'active' : ''}>AI Assistant</Link></li>
          </ul>
        )}

        <div className="navbar-actions">
          {isAuthenticated ? (
            <>
              <Link to="/notifications" className={`navbar-icon-btn notif-btn ${isActive('/notifications') ? 'active' : ''}`} title="Notifications" onClick={() => setUnreadCount(0)}>
                <Bell size={18} />
                {unreadCount > 0 && <span className="notif-badge">{unreadCount > 99 ? '99+' : unreadCount}</span>}
              </Link>
              <div className="navbar-user" onClick={() => setMenuOpen(!menuOpen)}>
                <div className="user-avatar">{user?.name?.[0]?.toUpperCase() || 'U'}</div>
                <span className="user-name">{user?.name?.split(' ')[0]}</span>
                <span className={`chevron ${menuOpen ? 'open' : ''}`}>▾</span>
                {menuOpen && (
                  <div className="user-dropdown">
                    <Link to="/dashboard" onClick={() => setMenuOpen(false)}><LayoutDashboard size={14} /> Dashboard</Link>
                    <Link to="/profile" onClick={() => setMenuOpen(false)}><User size={14} /> Profile</Link>
                    <Link to="/saved" onClick={() => setMenuOpen(false)}><Bookmark size={14} /> Saved Schemes</Link>
                    <div className="dropdown-divider" />
                    <button onClick={handleLogout}><LogOut size={14} /> Logout</button>
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
