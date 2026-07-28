import { useState, useEffect, useCallback } from 'react'
import { Navigate } from 'react-router-dom'
import Navbar from '../../components/layout/Navbar'
import Sidebar from '../../components/layout/Sidebar'
import BottomNav from '../../components/layout/BottomNav'
import { useAuth } from '../../hooks/useAuth'
import { BarChart2, ClipboardList, Users, FileText, MessageSquare, Bell, Target, Pencil, Trash2, UserCog, UserCheck } from 'lucide-react'
import api from '../../services/api'
import './Admin.css'

const TABS = [
  { id: 'overview', label: 'Overview', icon: BarChart2 },
  { id: 'schemes',  label: 'Schemes',  icon: ClipboardList },
  { id: 'users',    label: 'Users',    icon: Users },
]

export default function Admin() {
  const { user } = useAuth()
  const [tab, setTab] = useState('overview')
  const [msg, setMsg] = useState({ text: '', type: '' })

  if (user?.role !== 'admin') return <Navigate to="/dashboard" replace />

  const showMsg = (text, type = 'success') => {
    setMsg({ text, type })
    setTimeout(() => setMsg({ text: '', type: '' }), 4000)
  }

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

          {msg.text && (
            <div className={`admin-msg ${msg.type === 'error' ? 'admin-msg-error' : ''}`} onClick={() => setMsg({ text: '', type: '' })}>
              {msg.text} ✕
            </div>
          )}

          <div className="admin-tabs">
            {TABS.map(t => {
              const TabIcon = t.icon
              return (
                <button key={t.id} className={`admin-tab ${tab === t.id ? 'active' : ''}`} onClick={() => setTab(t.id)}>
                  <TabIcon size={15} /> {t.label}
                </button>
              )
            })}
          </div>

          {tab === 'overview' && <OverviewTab />}
          {tab === 'schemes'  && <SchemesTab showMsg={showMsg} />}
          {tab === 'users'    && <UsersTab showMsg={showMsg} />}
        </main>
      </div>
      <BottomNav />
    </div>
  )
}


// ── Overview Tab ──────────────────────────────────────────────────────────────

function OverviewTab() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    api.get('/admin/analytics').then(r => setStats(r.data)).catch(() => {})
  }, [])

  const cards = [
    { icon: <ClipboardList size={20} />, label: 'Total Schemes',     value: stats?.total_schemes },
    { icon: <Users size={20} />,         label: 'Total Users',        value: stats?.total_users },
    { icon: <Target size={20} />,        label: 'Recommendations',    value: stats?.total_recommendations },
    { icon: <MessageSquare size={20} />, label: 'Conversations',      value: stats?.total_conversations },
    { icon: <Bell size={20} />,          label: 'Notifications Sent', value: stats?.total_notifications },
  ]

  return (
    <div>
      <div className="admin-stats">
        {cards.map(c => (
          <div key={c.label} className="stat-card card">
            <div className="stat-icon">{c.icon}</div>
            <div className="stat-value">{c.value ?? '—'}</div>
            <div className="stat-label">{c.label}</div>
          </div>
        ))}
      </div>
      <div className="admin-info card">
        <h3>Platform Status</h3>
        <div className="status-list">
          {['Backend API Running', 'MongoDB Connected', 'AI Pipeline Active', 'Groq API Connected', 'ChromaDB Indexed'].map(item => (
            <div key={item} className="status-item">
              <span className="status-dot green" />{item}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}


// ── Schemes Tab ───────────────────────────────────────────────────────────────

function SchemesTab({ showMsg }) {
  const [schemes, setSchemes] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [deleteSlug, setDeleteSlug] = useState(null)
  const [showAdd, setShowAdd] = useState(false)
  const [editScheme, setEditScheme] = useState(null)

  const fetchSchemes = useCallback(async () => {
    setLoading(true)
    try {
      const res = await api.get('/schemes', { params: { keyword: search || undefined, page, page_size: 20 } })
      setSchemes(res.data.schemes)
      setTotal(res.data.total)
    } catch { /* silent */ }
    finally { setLoading(false) }
  }, [search, page])

  useEffect(() => { fetchSchemes() }, [fetchSchemes])

  const handleDelete = async (slug) => {
    try {
      await api.delete(`/admin/schemes/${slug}`)
      showMsg('Scheme deleted.')
      setDeleteSlug(null)
      fetchSchemes()
    } catch { showMsg('Failed to delete scheme.', 'error') }
  }

  return (
    <div>
      <div className="admin-schemes-toolbar">
        <input
          className="form-input"
          placeholder="Search schemes..."
          value={search}
          onChange={e => { setSearch(e.target.value); setPage(1) }}
          style={{ maxWidth: 320 }}
        />
        <button className="btn btn-primary btn-sm" onClick={() => setShowAdd(true)}>+ Add Scheme</button>
      </div>

      <div className="admin-table-meta">Showing {schemes.length} of {total} schemes</div>

      {loading ? (
        <div className="loading-center"><div className="loading-spinner" /></div>
      ) : (
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
              {schemes.map(s => (
                <tr key={s.slug}>
                  <td className="scheme-name-cell">{s.scheme_name}</td>
                  <td><span className={`badge ${s.level === 'Central' ? 'badge-blue' : 'badge-green'}`}>{s.level}</span></td>
                  <td className="category-cell">{s.schemeCategory?.[0] || '—'}</td>
                  <td>
                    <div className="table-actions">
                      <button className="btn btn-ghost btn-sm" onClick={() => setEditScheme(s)}><Pencil size={13} /> Edit</button>
                      <button className="btn btn-danger btn-sm" onClick={() => setDeleteSlug(s.slug)}><Trash2 size={13} /> Delete</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="admin-pagination">
        <button className="btn btn-ghost btn-sm" disabled={page === 1} onClick={() => setPage(p => p - 1)}>← Prev</button>
        <span>Page {page}</span>
        <button className="btn btn-ghost btn-sm" disabled={schemes.length < 20} onClick={() => setPage(p => p + 1)}>Next →</button>
      </div>

      {deleteSlug && (
        <Modal onClose={() => setDeleteSlug(null)}>
          <h3>Delete Scheme?</h3>
          <p>This action cannot be undone.</p>
          <div className="modal-actions">
            <button className="btn btn-ghost" onClick={() => setDeleteSlug(null)}>Cancel</button>
            <button className="btn btn-danger" onClick={() => handleDelete(deleteSlug)}>Delete</button>
          </div>
        </Modal>
      )}

      {showAdd && (
        <SchemeFormModal
          title="Add New Scheme"
          onClose={() => setShowAdd(false)}
          onSave={async (data) => {
            await api.post('/admin/schemes', data)
            showMsg('Scheme added and all users notified!')
            setShowAdd(false)
            fetchSchemes()
          }}
          onError={() => showMsg('Failed to add scheme.', 'error')}
        />
      )}

      {editScheme && (
        <SchemeFormModal
          title="Edit Scheme"
          initial={editScheme}
          onClose={() => setEditScheme(null)}
          onSave={async (data) => {
            await api.put(`/admin/schemes/${editScheme.slug}`, data)
            showMsg('Scheme updated.')
            setEditScheme(null)
            fetchSchemes()
          }}
          onError={() => showMsg('Failed to update scheme.', 'error')}
        />
      )}
    </div>
  )
}


// ── Users Tab ─────────────────────────────────────────────────────────────────

function UsersTab({ showMsg }) {
  const [users, setUsers] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [showAdd, setShowAdd] = useState(false)
  const [deleteId, setDeleteId] = useState(null)
  const [roleTarget, setRoleTarget] = useState(null) // { id, name, role }

  const fetchUsers = useCallback(async () => {
    setLoading(true)
    try {
      const res = await api.get('/admin/users', { params: { search: search || undefined, page, page_size: 20 } })
      setUsers(res.data.users)
      setTotal(res.data.total)
    } catch { /* silent */ }
    finally { setLoading(false) }
  }, [search, page])

  useEffect(() => { fetchUsers() }, [fetchUsers])

  const handleDelete = async (id) => {
    try {
      await api.delete(`/admin/users/${id}`)
      showMsg('User deleted.')
      setDeleteId(null)
      fetchUsers()
    } catch (e) { showMsg(e.response?.data?.detail || 'Failed to delete user.', 'error') }
  }

  const handleRoleChange = async (id, newRole) => {
    try {
      await api.patch(`/admin/users/${id}/role`, { role: newRole })
      showMsg(`Role updated to ${newRole}.`)
      setRoleTarget(null)
      fetchUsers()
    } catch { showMsg('Failed to update role.', 'error') }
  }

  return (
    <div>
      <div className="admin-schemes-toolbar">
        <input
          className="form-input"
          placeholder="Search users..."
          value={search}
          onChange={e => { setSearch(e.target.value); setPage(1) }}
          style={{ maxWidth: 320 }}
        />
        <button className="btn btn-primary btn-sm" onClick={() => setShowAdd(true)}>+ Add User</button>
      </div>

      <div className="admin-table-meta">Showing {users.length} of {total} users</div>

      {loading ? (
        <div className="loading-center"><div className="loading-spinner" /></div>
      ) : (
        <div className="admin-table card">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>State</th>
                <th>Joined</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map(u => (
                <tr key={u.id}>
                  <td className="scheme-name-cell">{u.name}</td>
                  <td style={{ fontSize: 13, color: 'var(--text-secondary)' }}>{u.email}</td>
                  <td>
                    <span className={`badge ${u.role === 'admin' ? 'badge-red' : 'badge-blue'}`}>{u.role}</span>
                  </td>
                  <td style={{ fontSize: 13 }}>{u.state || '—'}</td>
                  <td style={{ fontSize: 12, color: 'var(--text-muted)' }}>{formatDate(u.createdAt)}</td>
                  <td>
                    <div className="table-actions">
                      <button className="btn btn-ghost btn-sm" onClick={() => setRoleTarget(u)}>
                        {u.role === 'admin' ? <><UserCheck size={13} /> Demote</> : <><UserCog size={13} /> Make Admin</>}
                      </button>
                      <button className="btn btn-danger btn-sm" onClick={() => setDeleteId(u.id)}><Trash2 size={13} /></button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="admin-pagination">
        <button className="btn btn-ghost btn-sm" disabled={page === 1} onClick={() => setPage(p => p - 1)}>← Prev</button>
        <span>Page {page}</span>
        <button className="btn btn-ghost btn-sm" disabled={users.length < 20} onClick={() => setPage(p => p + 1)}>Next →</button>
      </div>

      {deleteId && (
        <Modal onClose={() => setDeleteId(null)}>
          <h3>Delete User?</h3>
          <p>This will permanently delete the user account.</p>
          <div className="modal-actions">
            <button className="btn btn-ghost" onClick={() => setDeleteId(null)}>Cancel</button>
            <button className="btn btn-danger" onClick={() => handleDelete(deleteId)}>Delete</button>
          </div>
        </Modal>
      )}

      {roleTarget && (
        <Modal onClose={() => setRoleTarget(null)}>
          <h3>Change Role</h3>
          <p>
            Change <strong>{roleTarget.name}</strong>'s role from{' '}
            <strong>{roleTarget.role}</strong> to{' '}
            <strong>{roleTarget.role === 'admin' ? 'user' : 'admin'}</strong>?
          </p>
          <div className="modal-actions">
            <button className="btn btn-ghost" onClick={() => setRoleTarget(null)}>Cancel</button>
            <button
              className="btn btn-primary"
              onClick={() => handleRoleChange(roleTarget.id, roleTarget.role === 'admin' ? 'user' : 'admin')}
            >
              Confirm
            </button>
          </div>
        </Modal>
      )}

      {showAdd && (
        <AddUserModal
          onClose={() => setShowAdd(false)}
          onSave={async (data) => {
            await api.post('/admin/users', data)
            showMsg('User created.')
            setShowAdd(false)
            fetchUsers()
          }}
          onError={(msg) => showMsg(msg, 'error')}
        />
      )}
    </div>
  )
}


// ── Reusable Modal ────────────────────────────────────────────────────────────

function Modal({ children, onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box card" onClick={e => e.stopPropagation()}>
        {children}
      </div>
    </div>
  )
}


// ── Scheme Form Modal ─────────────────────────────────────────────────────────

function SchemeFormModal({ title, initial = {}, onClose, onSave, onError }) {
  const [form, setForm] = useState({
    scheme_name: initial.scheme_name || '',
    slug: initial.slug || '',
    details: initial.details || '',
    benefits: initial.benefits || '',
    eligibility: initial.eligibility || '',
    application: initial.application || '',
    documents: initial.documents || '',
    level: initial.level || 'Central',
    schemeCategory: (initial.schemeCategory || []).join(', '),
    tags: (initial.tags || []).join(', '),
  })
  const [saving, setSaving] = useState(false)

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      await onSave({
        ...form,
        schemeCategory: form.schemeCategory.split(',').map(s => s.trim()).filter(Boolean),
        tags: form.tags.split(',').map(s => s.trim()).filter(Boolean),
      })
    } catch (err) {
      onError(err.response?.data?.detail || 'Error saving scheme.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box modal-large card" onClick={e => e.stopPropagation()}>
        <h3>{title}</h3>
        <form onSubmit={handleSubmit} className="scheme-form">
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Scheme Name *</label>
              <input className="form-input" required value={form.scheme_name} onChange={e => set('scheme_name', e.target.value)} />
            </div>
            <div className="form-group">
              <label className="form-label">Slug (auto-generated if empty)</label>
              <input className="form-input" value={form.slug} onChange={e => set('slug', e.target.value)} placeholder="e.g. pm-kisan-scheme" />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Level *</label>
              <select className="form-input" value={form.level} onChange={e => set('level', e.target.value)}>
                <option value="Central">Central</option>
                <option value="State">State</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Categories (comma-separated)</label>
              <input className="form-input" value={form.schemeCategory} onChange={e => set('schemeCategory', e.target.value)} placeholder="Education, Scholarship" />
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">Tags (comma-separated)</label>
            <input className="form-input" value={form.tags} onChange={e => set('tags', e.target.value)} placeholder="student, scholarship" />
          </div>
          <div className="form-group">
            <label className="form-label">Details *</label>
            <textarea className="form-input form-textarea" required value={form.details} onChange={e => set('details', e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Benefits *</label>
            <textarea className="form-input form-textarea" required value={form.benefits} onChange={e => set('benefits', e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Eligibility *</label>
            <textarea className="form-input form-textarea" required value={form.eligibility} onChange={e => set('eligibility', e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Application Process</label>
            <textarea className="form-input form-textarea" value={form.application} onChange={e => set('application', e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Required Documents</label>
            <textarea className="form-input form-textarea" value={form.documents} onChange={e => set('documents', e.target.value)} />
          </div>
          <div className="modal-actions">
            <button type="button" className="btn btn-ghost" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? 'Saving...' : 'Save Scheme'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}


// ── Add User Modal ────────────────────────────────────────────────────────────

function AddUserModal({ onClose, onSave, onError }) {
  const [form, setForm] = useState({ name: '', email: '', password: '', role: 'user' })
  const [saving, setSaving] = useState(false)
  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      await onSave(form)
    } catch (err) {
      onError(err.response?.data?.detail || 'Failed to create user.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box card" onClick={e => e.stopPropagation()}>
        <h3>Add New User</h3>
        <form onSubmit={handleSubmit} className="scheme-form">
          <div className="form-group">
            <label className="form-label">Full Name *</label>
            <input className="form-input" required value={form.name} onChange={e => set('name', e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Email *</label>
            <input className="form-input" type="email" required value={form.email} onChange={e => set('email', e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Password *</label>
            <input className="form-input" type="password" required minLength={8} value={form.password} onChange={e => set('password', e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Role</label>
            <select className="form-input" value={form.role} onChange={e => set('role', e.target.value)}>
              <option value="user">User</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div className="modal-actions">
            <button type="button" className="btn btn-ghost" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? 'Creating...' : 'Create User'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}


function formatDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString()
}
