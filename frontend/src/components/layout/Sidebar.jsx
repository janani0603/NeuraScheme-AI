import { NavLink } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { useSidebar } from '../../context/SidebarContext'
import { LayoutDashboard, Search, CheckCircle, Bot, Bookmark, Bell, User, Settings, PanelLeftClose, PanelLeftOpen } from 'lucide-react'
import './Sidebar.css'

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/explore', icon: Search, label: 'Explore Schemes' },
  { to: '/eligibility', icon: CheckCircle, label: 'Eligibility Checker' },
  { to: '/assistant', icon: Bot, label: 'AI Assistant' },
  { to: '/saved', icon: Bookmark, label: 'Saved Schemes' },
  { to: '/notifications', icon: Bell, label: 'Notifications' },
  { to: '/profile', icon: User, label: 'Profile' },
]

export default function Sidebar() {
  const { user } = useAuth()
  const { sidebarOpen, toggleSidebar } = useSidebar()

  return (
    <aside className={`sidebar ${sidebarOpen ? 'open' : 'collapsed'}`}>
      <button
        type="button"
        className="sidebar-toggle"
        onClick={toggleSidebar}
        aria-label={sidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
      >
        {sidebarOpen ? <PanelLeftClose size={18} /> : <PanelLeftOpen size={18} />}
      </button>

      <div className="sidebar-user">
        <div className="sidebar-avatar">{user?.name?.[0]?.toUpperCase() || 'U'}</div>
        <div className="sidebar-user-info">
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
            title={item.label}
          >
            <span className="sidebar-icon"><item.icon size={18} /></span>
            <span className="sidebar-label">{item.label}</span>
          </NavLink>
        ))}

        {user?.role === 'admin' && (
          <>
            <div className="sidebar-divider" />
            <NavLink to="/admin" className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}>
              <span className="sidebar-icon"><Settings size={18} /></span>
              <span>Admin Panel</span>
            </NavLink>
          </>
        )}
      </nav>
    </aside>
  )
}
