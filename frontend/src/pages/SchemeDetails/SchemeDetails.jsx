import { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import Navbar from '../../components/layout/Navbar'
import Sidebar from '../../components/layout/Sidebar'
import BottomNav from '../../components/layout/BottomNav'
import { useAuth } from '../../hooks/useAuth'
import api from '../../services/api'
import './SchemeDetails.css'

const TABS = ['Overview', 'Benefits', 'Eligibility', 'Documents', 'How to Apply']

export default function SchemeDetails() {
  const { slug } = useParams()
  const navigate = useNavigate()
  const { isAuthenticated, user, updateUser } = useAuth()
  const [scheme, setScheme] = useState(null)
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState(0)
  const [error, setError] = useState('')
  const [saved, setSaved] = useState(false)
  const [saving, setSaving] = useState(false)
  const [copyMsg, setCopyMsg] = useState('')

  useEffect(() => {
    api.get(`/schemes/${slug}`)
      .then((r) => {
        setScheme(r.data)
        setSaved(user?.saved_schemes?.includes(r.data.slug) || false)
      })
      .catch(() => setError('Scheme not found'))
      .finally(() => setLoading(false))
  }, [slug])

  const toggleSave = async () => {
    if (!isAuthenticated || saving) return
    setSaving(true)
    try {
      if (saved) {
        await api.delete(`/schemes/${slug}/save`)
        setSaved(false)
        updateUser({ ...user, saved_schemes: (user?.saved_schemes || []).filter(s => s !== slug) })
      } else {
        await api.post(`/schemes/${slug}/save`)
        setSaved(true)
        updateUser({ ...user, saved_schemes: [...(user?.saved_schemes || []), slug] })
      }
    } catch {
      // silently fail
    } finally {
      setSaving(false)
    }
  }

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href)
    setCopyMsg('Link copied!')
    setTimeout(() => setCopyMsg(''), 2000)
  }

  const handleAskAI = () => {
    navigate('/assistant', { state: { schemeSlug: slug, schemeName: scheme?.scheme_name } })
  }

  const content = (
    <main className={`page-content ${!isAuthenticated ? 'no-sidebar' : ''}`}>
      {loading ? (
        <div className="loading-center"><div className="loading-spinner" /></div>
      ) : error ? (
        <div className="empty-state">
          <div className="empty-icon">😕</div>
          <h3>{error}</h3>
          <Link to="/explore" className="btn btn-primary" style={{ marginTop: 16 }}>Back to Explorer</Link>
        </div>
      ) : scheme ? (
        <>
          {/* Breadcrumb */}
          <div className="breadcrumb">
            <Link to="/explore">Explore</Link>
            <span>›</span>
            <span>{scheme.scheme_name}</span>
          </div>

          <div className="scheme-detail-header card">
            <div className="sdh-top">
              <div className="sdh-badges">
                <span className={`badge ${scheme.level === 'Central' ? 'badge-blue' : 'badge-green'}`}>{scheme.level}</span>
                {scheme.schemeCategory?.map((c) => <span key={c} className="badge badge-gray">{c}</span>)}
              </div>
              {isAuthenticated && (
                <div className="sdh-actions">
                  <button className={`btn btn-sm ${saved ? 'btn-danger' : 'btn-outline'}`} onClick={toggleSave} disabled={saving}>
                    {saved ? '❤️ Saved' : '🤍 Save'}
                  </button>
                  <button className="btn btn-ghost btn-sm" onClick={handleShare}>
                    {copyMsg || '🔗 Share'}
                  </button>
                  <button className="btn btn-primary btn-sm" onClick={handleAskAI}>
                    🤖 Ask AI
                  </button>
                </div>
              )}
            </div>

            <h1 className="sdh-title">{scheme.scheme_name}</h1>

            <div className="sdh-tags">
              {scheme.tags?.map((t) => <span key={t} className="scheme-tag">#{t}</span>)}
            </div>

            {!isAuthenticated && (
              <div className="sdh-login-nudge">
                <span>🔐 <Link to="/login">Sign in</Link> to check your eligibility, save this scheme, and get AI guidance.</span>
              </div>
            )}
          </div>

          <div className="scheme-tabs card">
            <div className="tabs-header">
              {TABS.map((t, i) => (
                <button key={t} className={`tab-btn ${tab === i ? 'active' : ''}`} onClick={() => setTab(i)}>{t}</button>
              ))}
            </div>
            <div className="tab-content">
              {tab === 0 && <div className="tab-text">{scheme.details || 'No details available.'}</div>}
              {tab === 1 && <div className="tab-text">{scheme.benefits || 'No benefits information available.'}</div>}
              {tab === 2 && (
                <div>
                  <div className="tab-text">{scheme.eligibility || 'No eligibility information available.'}</div>
                  {isAuthenticated && (
                    <div className="elig-cta">
                      <p>Want to know if you qualify?</p>
                      <Link to="/eligibility" className="btn btn-primary btn-sm">✅ Check My Eligibility</Link>
                    </div>
                  )}
                </div>
              )}
              {tab === 3 && (
                <div>
                  <div className="tab-text">{scheme.documents || 'No document information available.'}</div>
                </div>
              )}
              {tab === 4 && (
                <div>
                  <div className="tab-text">{scheme.application || 'No application information available.'}</div>
                  {isAuthenticated && (
                    <div className="elig-cta">
                      <p>Need help with the application process?</p>
                      <button className="btn btn-primary btn-sm" onClick={handleAskAI}>🤖 Ask AI Assistant</button>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </>
      ) : null}
    </main>
  )

  return (
    <div>
      <Navbar />
      <div className="page-layout">
        {isAuthenticated && <Sidebar />}
        {content}
      </div>
      {isAuthenticated && <BottomNav />}
    </div>
  )
}
