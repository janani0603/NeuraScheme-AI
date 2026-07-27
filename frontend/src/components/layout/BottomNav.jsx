import { NavLink } from 'react-router-dom'
import './BottomNav.css'

const items = [
  { to: '/dashboard', icon: '🏠', label: 'Home' },
  { to: '/explore', icon: '🔍', label: 'Explore' },
  { to: '/eligibility', icon: '✅', label: 'Check' },
  { to: '/assistant', icon: '🤖', label: 'AI' },
  { to: '/profile', icon: '👤', label: 'Profile' },
]

export default function BottomNav() {
  return (
    <nav className="bottom-nav">
      {items.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          className={({ isActive }) => `bottom-nav-item ${isActive ? 'active' : ''}`}
        >
          <span className="bottom-nav-icon">{item.icon}</span>
          <span className="bottom-nav-label">{item.label}</span>
        </NavLink>
      ))}
    </nav>
  )
}
