import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import api from '../../services/api'
import './SchemeCard.css'

export default function SchemeCard({ scheme, showScore = false, onUnsave }) {
  const { isAuthenticated, user, updateUser } = useAuth()
  const [saved, setSaved] = useState(() => user?.saved_schemes?.includes(scheme.slug))
  const [saving, setSaving] = useState(false)

  const eligScore = scheme.eligibility_score
  const confScore = scheme.confidence_score
  const displayScore = eligScore ?? confScore
  const scoreColor = displayScore >= 75 ? 'score-high' : displayScore >= 50 ? 'score-medium' : 'score-low'

  const confidenceLabel = confScore >= 90 ? '★★★★★ Excellent Match'
    : confScore >= 75 ? '★★★★☆ Strong Match'
    : confScore >= 60 ? '★★★☆☆ Moderate Match'
    : confScore != null ? '★★☆☆☆ Weak Match' : null

  const toggleSave = async (e) => {
    e.preventDefault()
    if (!isAuthenticated || saving) return
    setSaving(true)
    try {
      if (saved) {
        await api.delete(`/schemes/${scheme.slug}/save`)
        setSaved(false)
        onUnsave?.(scheme.slug)
        updateUser({ ...user, saved_schemes: (user?.saved_schemes || []).filter(s => s !== scheme.slug) })
      } else {
        await api.post(`/schemes/${scheme.slug}/save`)
        setSaved(true)
        updateUser({ ...user, saved_schemes: [...(user?.saved_schemes || []), scheme.slug] })
      }
    } catch {
      // silently fail
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="scheme-card card">
      <div className="scheme-card-header">
        <div className="scheme-card-badges">
          <span className={`badge ${scheme.level === 'Central' ? 'badge-blue' : 'badge-green'}`}>
            {scheme.level}
          </span>
          {scheme.schemeCategory?.[0] && (
            <span className="badge badge-gray">{scheme.schemeCategory[0]}</span>
          )}
        </div>
        <div className="scheme-card-actions">
          {showScore && displayScore != null && (
            <span className={`score-value ${scoreColor}`}>{Math.round(displayScore)}%</span>
          )}
          {isAuthenticated && (
            <button
              className={`save-btn ${saved ? 'saved' : ''}`}
              onClick={toggleSave}
              disabled={saving}
              title={saved ? 'Remove from saved' : 'Save scheme'}
            >
              {saved ? '❤️' : '🤍'}
            </button>
          )}
        </div>
      </div>

      <h3 className="scheme-card-title">{scheme.scheme_name}</h3>
      <p className="scheme-card-desc">
        {scheme.details?.slice(0, 120)}{scheme.details?.length > 120 ? '...' : ''}
      </p>

      {showScore && displayScore != null && (
        <div className="scheme-card-bar">
          <div className="score-bar">
            <div className={`score-bar-fill ${scoreColor}`} style={{ width: `${displayScore}%` }} />
          </div>
          <div className="score-bar-labels">
            <span className="score-label">Eligibility Score</span>
            {confScore != null && <span className={`conf-label ${scoreColor}`}>{confidenceLabel}</span>}
          </div>
        </div>
      )}

      {/* Matched / Missing conditions */}
      {scheme.matched_conditions?.length > 0 && (
        <div className="conditions">
          {scheme.matched_conditions.slice(0, 3).map((c) => (
            <span key={c} className="condition matched">✓ {c}</span>
          ))}
          {scheme.missing_conditions?.slice(0, 2).map((c) => (
            <span key={c} className="condition missing">✗ {c}</span>
          ))}
        </div>
      )}

      {scheme.explanation && (
        <p className="scheme-card-explanation">💡 {scheme.explanation}</p>
      )}

      <div className="scheme-card-footer">
        <div className="scheme-tags">
          {scheme.tags?.slice(0, 3).map((tag) => (
            <span key={tag} className="scheme-tag">#{tag}</span>
          ))}
        </div>
        <Link to={`/schemes/${scheme.slug}`} className="btn btn-primary btn-sm">
          View Details
        </Link>
      </div>
    </div>
  )
}
