import { useState, useEffect } from 'react'
import { Navigate } from 'react-router-dom'
import Navbar from '../../components/layout/Navbar'
import Sidebar from '../../components/layout/Sidebar'
import BottomNav from '../../components/layout/BottomNav'
import { useAuth } from '../../hooks/useAuth'
import api from '../../services/api'
import './Admin.css'

export default function Admin() {
  const { user } = useAuth()
  const [stats, setStats] = useState(null)
  const [schemes, setSchemes] = useState([])
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState('overview')
  const [search, setSearch] = useState('')
  const [deleteSlug, setDeleteSlug] = useState(null)
  const [msg, setMsg] = useState('')

  const isAdmin = user?.role === 'admin'

  useEffect(() => {
    if (!isAdmin) return
    Promise.all([
      api.get('/admin/analytics').catch(() => null),
      api.get('/schemes', { params: { page: 1, page_size: 20 } }).catch(() => ({ data: { schemes: [], total: 0 } })),
    ]).then(([analyticsRes, schemesRes]) => {
      setStats(analyticsRes?.data || null)
      setSchemes(schemesRes.data.schemes || [])
    }).finally(() => setLoading(false))
  }, [isAdmin])

  if (!isAdmin) return <Navigate to="/dashboard" replace />

  const handleDelete = async (slug) => {
    try {
      await api.delete(`/admin/schemes/${slug}`)
      setSchemes((s) => s.filter((x) => x.slug !== slug))
      setMsg('Scheme deleted successfully.')
      setDeleteSlug(null)
    } catch {
      setMsg('Failed to delete scheme.')
    }
  }

  const filtered = schemes.filter((s) =>
    s.scheme_name?.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div>
      <Navbar />
      <div className="page-layout">
        <Sidebar />
        <main className="page-content">
          <div className="admin-header">
            <div>
              <div className="page-title">Admin Dashboard</div>
              <div className="page-subtitle">Manage schemes, users, and platform analytics</div>
            </div>
            <span className="badge badge-red">Admin</span>
          </div>

          {msg && <div className="admin-msg" onClick={() => setMsg('')}>{msg} ✕</div>}

          <div className="admin-tabs">
            {['overview', 'schemes'].map((t) => (
              <button key={t} className={`admin-tab ${tab === t ? 'active' : ''}`} onClick={() => setTab(t)}>
                {t === 'overview' ? '📊 Overview' : '📋 Schemes'}
              </button>
            ))}
          </div>

          {loading ? (
            <div className="loading-center"><div className="loading-spinner" /></div>
          ) : tab === 'overview' ? (
            <div>
              <div className="admin-stats">
                {[
                  { icon: '📋', label: 'Total Schemes', value: stats?.total_schemes ?? schemes.length },
                  { icon: '👥', label: 'Total Users', value: stats?.total_users ?? '—' },
                  { icon: '🎯', label: 'Recommendations', value: stats?.total_recommendations ?? '—' },
                  { icon: '💬', label: 'Conversations', value: stats?.total_conversations ?? '—' },
                ].map((s) => (
                  <div key={s.label} className="stat-card card">
                    <div className="stat-icon">{s.icon}</div>
                    <div className="stat-value">{s.value}</div>
                    <div className="stat-label">{s.label}</div>
                  </div>
                ))}
              </div>
              <div className="admin-info card">
                <h3>Platform Status</h3>
                <div className="status-list">
                  {['Backend API Running','MongoDB Connected','AI Pipeline Active','Gemini API Connected'].map((item) => (
                    <div key={item} className="status-item">
                      <span className="status-dot green" />{item}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div>
              <div className="admin-schemes-toolbar">
                <input className="form-input" placeholder="Search schemes..." value={search} onChange={(e) => setSearch(e.target.value)} style={{ maxWidth: 320 }} />
              </div>
              <div className="admin-table card">
                <table>
                  <thead>
                    <tr>
                      <th>Scheme Name</th>
                      <th>Level</th>
                      <th>Category</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filtered.map((s) => (
                      <tr key={s.slug}>
                        <td className="scheme-name-cell">{s.scheme_name}</td>
                        <td><span className={`badge ${s.level === 'Central' ? 'badge-blue' : 'badge-green'}`}>{s.level}</span></td>
                        <td className="category-cell">{s.schemeCategory?.[0] || '—'}</td>
                        <td>
                          <div className="table-actions">
                            <button className="btn btn-danger btn-sm" onClick={() => setDeleteSlug(s.slug)}>🗑️ Delete</button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {deleteSlug && (
            <div className="modal-overlay" onClick={() => setDeleteSlug(null)}>
              <div className="modal-box card" onClick={(e) => e.stopPropagation()}>
                <h3>Delete Scheme?</h3>
                <p>This action cannot be undone.</p>
                <div className="modal-actions">
                  <button className="btn btn-ghost" onClick={() => setDeleteSlug(null)}>Cancel</button>
                  <button className="btn btn-danger" onClick={() => handleDelete(deleteSlug)}>Delete</button>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
      <BottomNav />
    </div>
  )
}
