import { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import Navbar from '../../components/layout/Navbar'
import Sidebar from '../../components/layout/Sidebar'
import BottomNav from '../../components/layout/BottomNav'
import { useAuth } from '../../hooks/useAuth'
import { Heart, Share2, Bot, FileText, CheckCircle, Lock, Frown } from 'lucide-react'
import api from '../../services/api'
import './SchemeDetails.css'

const TABS = ['Overview', 'Benefits', 'Eligibility', 'Documents', 'How to Apply']

function parseLines(text) {
  if (!text) return []
  const byNewline = text.split(/\n+/).map((l) => l.trim()).filter((l) => l.length > 6)
  if (byNewline.length > 1) {
    return byNewline.map((l) => l.replace(/^[\d.)-]+\s*/, '').trim()).filter((l) => l.length > 6)
  }
  return text
    .split(/\.\s+(?=[A-Z])/)
    .map((l) => l.replace(/^[\d.)-]+\s*/, '').trim())
    .filter((l) => l.length > 6)
}

function StepList({ text }) {
  const steps = parseLines(text)
  if (!steps.length) return <div className="tab-text">{text || 'No information available.'}</div>
  return (
    <ol className="steps-list">
      {steps.map((s, i) => (
        <li key={i} className="step-item">
          <div className="step-num">{i + 1}</div>
          <div className="step-text">{s}</div>
        </li>
      ))}
    </ol>
  )
}

function DocList({ text }) {
  const lines = text
    ? text.split(/\n|[,;]/).map((l) => l.replace(/^[-•*]+\s*/, '').trim()).filter((l) => l.length > 3)
    : []
  if (!lines.length) return <div className="tab-text">{text || 'No information available.'}</div>
  return (
    <ul className="doc-list">
      {lines.map((d, i) => (
        <li key={i} className="doc-item">
          <span className="doc-icon"><FileText size={14} /></span>
          <span>{d}</span>
        </li>
      ))}
    </ul>
  )
}

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
          <div className="empty-icon"><Frown size={40} strokeWidth={1.5} /></div>
          <h3>{error}</h3>
          <Link to="/explore" className="btn btn-primary" style={{ marginTop: 16 }}>Back to Explorer</Link>
        </div>
      ) : scheme ? (
        <>
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
                    <Heart size={14} fill={saved ? 'currentColor' : 'none'} /> {saved ? 'Saved' : 'Save'}
                  </button>
                  <button className="btn btn-ghost btn-sm" onClick={handleShare}>
                    <Share2 size={14} /> {copyMsg || 'Share'}
                  </button>
                  <button className="btn btn-primary btn-sm" onClick={handleAskAI}>
                    <Bot size={14} /> Ask AI
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
                <Lock size={14} /> <Link to="/login">Sign in</Link> to check your eligibility, save this scheme, and get AI guidance.
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
              {tab === 0 && <StepList text={scheme.details} />}
              {tab === 1 && <StepList text={scheme.benefits} />}
              {tab === 2 && (
                <div>
                  <StepList text={scheme.eligibility} />
                  {isAuthenticated && (
                    <div className="elig-cta">
                      <p>Want to know if you qualify?</p>
                      <Link to="/eligibility" className="btn btn-primary btn-sm">
                        <CheckCircle size={14} /> Check My Eligibility
                      </Link>
                    </div>
                  )}
                </div>
              )}
              {tab === 3 && <DocList text={scheme.documents} />}
              {tab === 4 && (
                <div>
                  <StepList text={scheme.application} />
                  {isAuthenticated && (
                    <div className="elig-cta">
                      <p>Need help with the application process?</p>
                      <button className="btn btn-primary btn-sm" onClick={handleAskAI}>
                        <Bot size={14} /> Ask AI Assistant
                      </button>
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
