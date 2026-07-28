import { useState, useEffect, useCallback } from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../../components/layout/Navbar'
import Sidebar from '../../components/layout/Sidebar'
import BottomNav from '../../components/layout/BottomNav'
import { Sparkles, Clock, RefreshCw, Megaphone, Bell, Check, Trash2 } from 'lucide-react'
import api from '../../services/api'
import './Notifications.css'

const TYPE_ICON = {
  new_scheme: Sparkles,
  deadline: Clock,
  update: RefreshCw,
  system: Megaphone,
}

export default function Notifications() {
  const [notifications, setNotifications] = useState([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')

  const fetchNotifications = useCallback(async () => {
    try {
      const res = await api.get('/notifications', {
        params: { unread_only: filter === 'unread' },
      })
      setNotifications(res.data.notifications)
      setUnreadCount(res.data.unread_count)
    } catch {
      // silent
    } finally {
      setLoading(false)
    }
  }, [filter])

  useEffect(() => {
    setLoading(true)
    fetchNotifications()
  }, [fetchNotifications])

  const handleRead = async (id) => {
    await api.patch(`/notifications/${id}/read`).catch(() => {})
    setNotifications(n => n.map(x => x.id === id ? { ...x, is_read: true } : x))
    setUnreadCount(c => Math.max(0, c - 1))
  }

  const handleDelete = async (id) => {
    await api.delete(`/notifications/${id}`).catch(() => {})
    setNotifications(n => n.filter(x => x.id !== id))
  }

  const handleMarkAllRead = async () => {
    await api.patch('/notifications/read-all').catch(() => {})
    setNotifications(n => n.map(x => ({ ...x, is_read: true })))
    setUnreadCount(0)
  }

  const displayed = filter === 'unread'
    ? notifications.filter(n => !n.is_read)
    : notifications

  return (
    <div>
      <Navbar />
      <div className="page-layout">
        <Sidebar />
        <main className="page-content">
          <div className="notif-header">
            <div>
              <div className="page-title">Notifications</div>
              <div className="page-subtitle">
                {unreadCount > 0 ? `${unreadCount} unread notification${unreadCount > 1 ? 's' : ''}` : 'All caught up!'}
              </div>
            </div>
            {unreadCount > 0 && (
              <button className="btn btn-ghost btn-sm" onClick={handleMarkAllRead}>
                <Check size={14} /> Mark all read
              </button>
            )}
          </div>

          <div className="notif-filters">
            {['all', 'unread'].map(f => (
              <button
                key={f}
                className={`filter-chip ${filter === f ? 'active' : ''}`}
                onClick={() => setFilter(f)}
              >
                {f === 'all' ? 'All' : `Unread${unreadCount > 0 ? ` (${unreadCount})` : ''}`}
              </button>
            ))}
          </div>

          {loading ? (
            <div className="loading-center"><div className="loading-spinner" /></div>
          ) : displayed.length === 0 ? (
            <div className="empty-state card">
              <div className="empty-icon"><Bell size={40} strokeWidth={1.5} /></div>
              <h3>{filter === 'unread' ? 'No unread notifications' : 'No notifications yet'}</h3>
              <p>You'll be notified about new schemes, deadlines, and updates here.</p>
            </div>
          ) : (
            <div className="notif-list">
              {displayed.map(n => {
                const IconComp = TYPE_ICON[n.type] || Megaphone
                return (
                  <div
                    key={n.id}
                    className={`notif-item card ${!n.is_read ? 'unread' : ''}`}
                    onClick={() => !n.is_read && handleRead(n.id)}
                  >
                    <div className="notif-icon"><IconComp size={18} /></div>
                    <div className="notif-body">
                      <div className="notif-title">{n.title}</div>
                      <div className="notif-message">{n.message}</div>
                      <div className="notif-meta">
                        <span className="notif-time">{formatTime(n.createdAt)}</span>
                        {n.scheme_slug && (
                          <Link
                            to={`/schemes/${n.scheme_slug}`}
                            className="notif-link"
                            onClick={e => e.stopPropagation()}
                          >
                            View Scheme →
                          </Link>
                        )}
                      </div>
                    </div>
                    <div className="notif-actions">
                      {!n.is_read && (
                        <button
                          className="notif-read-btn"
                          onClick={e => { e.stopPropagation(); handleRead(n.id) }}
                          title="Mark as read"
                        >
                          <Check size={12} />
                        </button>
                      )}
                      {!n.is_read && <span className="unread-dot" />}
                      <button
                        className="notif-delete-btn"
                        onClick={e => { e.stopPropagation(); handleDelete(n.id) }}
                        title="Delete"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </main>
      </div>
      <BottomNav />
    </div>
  )
}

function formatTime(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  const now = new Date()
  const diff = Math.floor((now - d) / 1000)
  if (diff < 60) return 'Just now'
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`
  return d.toLocaleDateString()
}
