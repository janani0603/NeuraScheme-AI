import { useState } from 'react'
import Navbar from '../../components/layout/Navbar'
import Sidebar from '../../components/layout/Sidebar'
import BottomNav from '../../components/layout/BottomNav'
import { useAuth } from '../../hooks/useAuth'
import api from '../../services/api'
import './Profile.css'

const STATES = ['Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Goa','Gujarat','Haryana','Himachal Pradesh','Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal','Delhi','Jammu & Kashmir','Ladakh','Puducherry']
const OCCUPATIONS = ['Student','Farmer','Government Employee','Private Employee','Self Employed','Business Owner','Unemployed','Homemaker','Retired','Other']
const EDUCATIONS = ['Below 10th','10th Pass','12th Pass','Diploma','Graduate','Post Graduate','PhD','Other']
const CATEGORIES = ['General','OBC','SC','ST','EWS']

export default function Profile() {
  const { user, updateUser } = useAuth()
  const [editing, setEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({ ...user })

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }))

  const save = async () => {
    setSaving(true)
    setError('')
    setSuccess(false)
    try {
      const res = await api.put('/users/me', form)
      updateUser(res.data)
      setSuccess(true)
      setEditing(false)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save changes')
    } finally {
      setSaving(false)
    }
  }

  const completeness = getCompleteness(user)

  return (
    <div>
      <Navbar />
      <div className="page-layout">
        <Sidebar />
        <main className="page-content">
          <div className="page-title">My Profile</div>
          <div className="page-subtitle">Manage your personal information</div>

          {/* Completeness */}
          <div className="profile-completeness card">
            <div className="completeness-header">
              <div>
                <strong>Profile Completeness</strong>
                <p>A complete profile gives better AI recommendations</p>
              </div>
              <span className="completeness-pct">{completeness}%</span>
            </div>
            <div className="score-bar" style={{ marginTop: 10 }}>
              <div className={`score-bar-fill ${completeness >= 75 ? 'score-high' : completeness >= 40 ? 'score-medium' : 'score-low'}`} style={{ width: `${completeness}%` }} />
            </div>
          </div>

          {success && <div className="profile-success">✅ Profile updated successfully!</div>}
          {error && <div className="auth-error">⚠️ {error}</div>}

          <div className="profile-card card">
            <div className="profile-card-header">
              <div className="profile-avatar-lg">{user?.name?.[0]?.toUpperCase()}</div>
              <div>
                <h2>{user?.name}</h2>
                <p>{user?.email}</p>
                <span className="badge badge-blue">{user?.role || 'user'}</span>
              </div>
              <button className="btn btn-outline btn-sm profile-edit-btn" onClick={() => { setEditing(!editing); setSuccess(false) }}>
                {editing ? '✕ Cancel' : '✏️ Edit Profile'}
              </button>
            </div>

            <div className="divider" />

            {editing ? (
              <div className="profile-form">
                <div className="profile-section">
                  <h3 className="profile-section-title">Personal Information</h3>
                  <div className="profile-grid">
                    <div className="form-group">
                      <label className="form-label">Full Name</label>
                      <input className="form-input" value={form.name || ''} onChange={(e) => set('name', e.target.value)} />
                    </div>
                    <div className="form-group">
                      <label className="form-label">Phone</label>
                      <input className="form-input" value={form.phone || ''} onChange={(e) => set('phone', e.target.value)} />
                    </div>
                    <div className="form-group">
                      <label className="form-label">Date of Birth</label>
                      <input type="date" className="form-input" value={form.date_of_birth || ''} onChange={(e) => set('date_of_birth', e.target.value)} />
                    </div>
                    <div className="form-group">
                      <label className="form-label">Gender</label>
                      <select className="form-select" value={form.gender || ''} onChange={(e) => set('gender', e.target.value)}>
                        <option value="">Select</option>
                        <option>Male</option><option>Female</option><option>Other</option>
                      </select>
                    </div>
                    <div className="form-group">
                      <label className="form-label">State</label>
                      <select className="form-select" value={form.state || ''} onChange={(e) => set('state', e.target.value)}>
                        <option value="">Select State</option>
                        {STATES.map((s) => <option key={s}>{s}</option>)}
                      </select>
                    </div>
                    <div className="form-group">
                      <label className="form-label">District</label>
                      <input className="form-input" value={form.district || ''} onChange={(e) => set('district', e.target.value)} />
                    </div>
                  </div>
                </div>

                <div className="divider" />

                <div className="profile-section">
                  <h3 className="profile-section-title">Professional Information</h3>
                  <div className="profile-grid">
                    <div className="form-group">
                      <label className="form-label">Occupation</label>
                      <select className="form-select" value={form.occupation || ''} onChange={(e) => set('occupation', e.target.value)}>
                        <option value="">Select</option>
                        {OCCUPATIONS.map((o) => <option key={o}>{o}</option>)}
                      </select>
                    </div>
                    <div className="form-group">
                      <label className="form-label">Education</label>
                      <select className="form-select" value={form.education || ''} onChange={(e) => set('education', e.target.value)}>
                        <option value="">Select</option>
                        {EDUCATIONS.map((e) => <option key={e}>{e}</option>)}
                      </select>
                    </div>
                    <div className="form-group">
                      <label className="form-label">Annual Income (₹)</label>
                      <input type="number" className="form-input" value={form.annual_income || ''} onChange={(e) => set('annual_income', e.target.value)} />
                    </div>
                    <div className="form-group">
                      <label className="form-label">Category</label>
                      <select className="form-select" value={form.category || ''} onChange={(e) => set('category', e.target.value)}>
                        <option value="">Select</option>
                        {CATEGORIES.map((c) => <option key={c}>{c}</option>)}
                      </select>
                    </div>
                  </div>
                  <div className="profile-checkboxes">
                    {[['is_student','Student'],['is_farmer','Farmer'],['is_business_owner','Business Owner'],['has_disability','Has Disability']].map(([k, label]) => (
                      <label key={k} className="elig-checkbox">
                        <input type="checkbox" checked={form[k] || false} onChange={(e) => set(k, e.target.checked)} />
                        {label}
                      </label>
                    ))}
                  </div>
                </div>

                <button className="btn btn-primary" style={{ marginTop: 20 }} onClick={save} disabled={saving}>
                  {saving ? 'Saving...' : '💾 Save Changes'}
                </button>
              </div>
            ) : (
              <div className="profile-view">
                <div className="profile-section">
                  <h3 className="profile-section-title">Personal Information</h3>
                  <div className="profile-grid">
                    {[
                      ['Name', user?.name],
                      ['Email', user?.email],
                      ['Phone', user?.phone],
                      ['Date of Birth', user?.date_of_birth],
                      ['Gender', user?.gender],
                      ['State', user?.state],
                      ['District', user?.district],
                    ].map(([label, val]) => (
                      <div key={label} className="profile-field">
                        <span className="field-label">{label}</span>
                        <span className="field-value">{val || <span className="field-empty">Not set</span>}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="divider" />
                <div className="profile-section">
                  <h3 className="profile-section-title">Professional Information</h3>
                  <div className="profile-grid">
                    {[
                      ['Occupation', user?.occupation],
                      ['Education', user?.education],
                      ['Annual Income', user?.annual_income ? `₹${Number(user.annual_income).toLocaleString()}` : null],
                      ['Category', user?.category],
                    ].map(([label, val]) => (
                      <div key={label} className="profile-field">
                        <span className="field-label">{label}</span>
                        <span className="field-value">{val || <span className="field-empty">Not set</span>}</span>
                      </div>
                    ))}
                  </div>
                  <div className="profile-flags">
                    {[['is_student','Student'],['is_farmer','Farmer'],['is_business_owner','Business Owner'],['has_disability','Has Disability']].map(([k, label]) => (
                      <span key={k} className={`badge ${user?.[k] ? 'badge-green' : 'badge-gray'}`}>{user?.[k] ? '✓' : '✗'} {label}</span>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
      <BottomNav />
    </div>
  )
}

function getCompleteness(user) {
  if (!user) return 0
  const fields = ['state', 'gender', 'occupation', 'education', 'annual_income', 'category', 'date_of_birth']
  const filled = fields.filter((f) => user[f]).length
  return Math.round((filled / fields.length) * 100)
}
