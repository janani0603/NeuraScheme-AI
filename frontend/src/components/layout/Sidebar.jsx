import { NavLink } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import './Sidebar.css'

const navItems = [
  { to: '/dashboard', icon: '🏠', label: 'Dashboard' },
  { to: '/explore', icon: '🔍', label: 'Explore Schemes' },
  { to: '/eligibility', icon: '✅', label: 'Eligibility Checker' },
  { to: '/assistant', icon: '🤖', label: 'AI Assistant' },
  { to: '/saved', icon: '❤️', label: 'Saved Schemes' },
  { to: '/notifications', icon: '🔔', label: 'Notifications' },
  { to: '/profile', icon: '👤', label: 'Profile' },
]

export default function Sidebar() {
  const { user } = useAuth()

  return (
    <aside className="sidebar">
      <div className="sidebar-user">
        <div className="sidebar-avatar">{user?.name?.[0]?.toUpperCase() || 'U'}</div>
        <div>
          <div className="sidebar-user-name">{user?.name || 'User'}</div>
          <div className="sidebar-user-email">{user?.email || ''}</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
          >
            <span className="sidebar-icon">{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}

        {user?.role === 'admin' && (
          <>
            <div className="sidebar-divider" />
            <NavLink to="/admin" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <span className="sidebar-icon">⚙️</span>
              <span>Admin Panel</span>
            </NavLink>
          </>
        )}
      </nav>
    </aside>
  )
}
