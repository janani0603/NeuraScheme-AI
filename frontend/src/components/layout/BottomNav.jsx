import { NavLink } from 'react-router-dom'
import { LayoutDashboard, Search, CheckCircle, Bot, User } from 'lucide-react'
import './BottomNav.css'

const items = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Home' },
  { to: '/explore', icon: Search, label: 'Explore' },
  { to: '/eligibility', icon: CheckCircle, label: 'Check' },
  { to: '/assistant', icon: Bot, label: 'AI' },
  { to: '/profile', icon: User, label: 'Profile' },
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
          <span className="bottom-nav-icon"><item.icon size={20} /></span>
          <span className="bottom-nav-label">{item.label}</span>
        </NavLink>
      ))}
    </nav>
  )
}
