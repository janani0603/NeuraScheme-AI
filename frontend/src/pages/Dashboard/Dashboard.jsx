import { useState, useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../../components/layout/Navbar'
import Sidebar from '../../components/layout/Sidebar'
import BottomNav from '../../components/layout/BottomNav'
import { useAuth } from '../../hooks/useAuth'
import { Target, Heart, BarChart2, CheckCircle, Brain, Search, Bot, Bookmark } from 'lucide-react'
import api from '../../services/api'
import './Dashboard.css'

function AnimatedStat({ value }) {
  const ref = useRef(null)
  const num = parseInt(value)
  const isNum = !isNaN(num)
  useEffect(() => {
    const el = ref.current
    if (!el || !isNum || num === 0) return
    let start
    const step = (ts) => {
      if (!start) start = ts
      const p = Math.min((ts - start) / 800, 1)
      el.textContent = String(value).includes('%')
        ? Math.floor(p * num) + '%'
        : Math.floor(p * num)
      if (p < 1) requestAnimationFrame(step)
      else el.textContent = value
    }
    requestAnimationFrame(step)
  }, [num, isNum, value])
  return <div className="stat-value" ref={ref}>{value}</div>
}

function ProfileRing({ completeness }) {
  const r = 36
  const circ = 2 * Math.PI * r
  const offset = circ - (completeness / 100) * circ
  const color = completeness >= 80 ? '#10B981' : completeness >= 50 ? '#F59E0B' : '#00C9B8'
  return (
    <div className="profile-ring-wrap">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="var(--border)" strokeWidth="6" />
        <circle
          cx="44" cy="44" r={r} fill="none"
          stroke={color} strokeWidth="6"
          strokeDasharray={circ} strokeDashoffset={offset}
          strokeLinecap="round"
          transform="rotate(-90 44 44)"
          style={{ transition: 'stroke-dashoffset 1s ease' }}
        />
      </svg>
      <div className="profile-ring-label">
        <span className="profile-ring-pct" style={{ color }}>{completeness}%</span>
        <span className="profile-ring-sub">complete</span>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const { user } = useAuth()
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(true)

  const hour = new Date().getHours()
  const greeting = hour < 12 ? 'Good Morning' : hour < 17 ? 'Good Afternoon' : 'Good Evening'

  useEffect(() => {
    api.get('/recommendations/me')
      .then((r) => setRecommendations(r.data.recommendations || []))
      .catch(() => setRecommendations([]))
      .finally(() => setLoading(false))
  }, [])

  const completeness = getCompleteness(user)
  const savedCount = user?.saved_schemes?.length || 0
  const topSchemes = recommendations.slice(0, 5)
  const avgScore = recommendations.length
    ? Math.round(recommendations.slice(0, 10).reduce((a, r) => a + (r.eligibility_score || 0), 0) / Math.min(recommendations.length, 10))
    : 0

  const stats = [
    { icon: <Target size={20} />, label: 'Matched Schemes', value: recommendations.length || '—', color: 'blue' },
    { icon: <Heart size={20} />, label: 'Saved', value: savedCount, color: 'red' },
    { icon: <BarChart2 size={20} />, label: 'Avg Score', value: avgScore ? avgScore + '%' : '—', color: 'green' },
    { icon: <CheckCircle size={20} />, label: 'Profile', value: completeness + '%', color: 'yellow' },
  ]

  const missingFields = getMissingFields(user)
  const aiInsights = getInsights(user, recommendations)

  return (
    <div>
      <Navbar />
      <div className="page-layout">
        <Sidebar />
        <main className="page-content">

          {/* Welcome Banner */}
          <div className="dashboard-welcome card">
            <div className="welcome-text">
              <h1>{greeting}, {user?.name?.split(' ')[0] || 'there'}</h1>
              <p>Here's your personalized government scheme overview.</p>
            </div>
            <div className="welcome-actions">
              <Link to="/eligibility" className="btn btn-primary">
                <Brain size={15} /> Run AI Check
              </Link>
              <Link to="/explore" className="btn btn-ghost">Explore Schemes</Link>
            </div>
          </div>

          {/* Stats */}
          <div className="dashboard-stats">
            {stats.map((s) => (
              <div key={s.label} className={`stat-card card stat-${s.color}`}>
                <div className="stat-icon">{s.icon}</div>
                <AnimatedStat value={String(s.value)} />
                <div className="stat-label">{s.label}</div>
              </div>
            ))}
          </div>

          <div className="dashboard-two-col">

            {/* Left column */}
            <div className="dashboard-section">

              <div className="section-title-row">
                <h2>Top Matched Schemes</h2>
                <Link to="/eligibility" className="btn btn-outline btn-sm">View All →</Link>
              </div>

              {loading ? (
                <div className="loading-center"><div className="loading-spinner" /></div>
              ) : topSchemes.length === 0 ? (
                <div className="empty-state card">
                  <div className="empty-icon"><Target size={40} strokeWidth={1.5} /></div>
                  <h3>No recommendations yet</h3>
                  <p>Run the eligibility checker to get AI-powered scheme recommendations.</p>
                  <Link to="/eligibility" className="btn btn-primary" style={{ marginTop: 16 }}>Check Eligibility</Link>
                </div>
              ) : (
                <div className="ranked-list card">
                  {topSchemes.map((r, i) => {
                    const score = r.eligibility_score || 0
                    const scoreClass = score >= 75 ? 'score-high' : score >= 50 ? 'score-medium' : 'score-low'
                    return (
                      <Link to={`/schemes/${r.slug}`} key={r.slug} className="ranked-item">
                        <div className="ranked-num">{i + 1}</div>
                        <div className="ranked-info">
                          <div className="ranked-name">{r.scheme_name}</div>
                          <div className="ranked-meta">
                            <span className={`badge ${r.level === 'Central' ? 'badge-blue' : 'badge-green'}`}>{r.level}</span>
                            {r.schemeCategory?.[0] && <span className="badge badge-gray">{r.schemeCategory[0]}</span>}
                          </div>
                          <div className="ranked-bar">
                            <div className="score-bar">
                              <div className={`score-bar-fill ${scoreClass}`} style={{ width: `${score}%` }} />
                            </div>
                          </div>
                        </div>
                        <div className={`ranked-score ${scoreClass}`}>{Math.round(score)}%</div>
                      </Link>
                    )
                  })}
                </div>
              )}

              {recommendations.length > 0 && (
                <>
                  <div className="section-title-row" style={{ marginTop: 28 }}>
                    <h2>Scheme Categories</h2>
                  </div>
                  <div className="category-breakdown card">
                    {getCategoryBreakdown(recommendations).map(({ cat, count, pct }) => (
                      <div key={cat} className="cat-row">
                        <div className="cat-label">{cat}</div>
                        <div className="cat-bar-wrap">
                          <div className="cat-bar">
                            <div className="cat-bar-fill" style={{ width: `${pct}%` }} />
                          </div>
                        </div>
                        <div className="cat-count">{count}</div>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>

            {/* Right column */}
            <div className="dashboard-right">

              {/* Profile Completeness */}
              <div className="profile-widget card">
                <div className="profile-widget-header">
                  <div>
                    <h3>Profile Strength</h3>
                    <p>{completeness < 100 ? `${missingFields.length} fields missing` : 'Profile complete!'}</p>
                  </div>
                  <ProfileRing completeness={completeness} />
                </div>
                {missingFields.length > 0 && (
                  <div className="missing-fields">
                    {missingFields.map((f) => (
                      <span key={f} className="missing-tag">+ {f}</span>
                    ))}
                  </div>
                )}
                <Link to="/profile" className="btn btn-primary btn-sm" style={{ width: '100%', justifyContent: 'center', marginTop: 12 }}>
                  {completeness < 100 ? 'Complete Profile' : 'View Profile'}
                </Link>
              </div>

              {/* AI Insights */}
              <div className="ai-insights card">
                <div className="insights-header">
                  <span className="insights-icon"><Brain size={18} /></span>
                  <h3>AI Insights</h3>
                </div>
                <div className="insights-list">
                  {aiInsights.map((insight, i) => (
                    <div key={i} className="insight-item">
                      <span className="insight-dot" />
                      <p>{insight}</p>
                    </div>
                  ))}
                </div>
                <Link to="/eligibility" className="btn btn-primary btn-sm insights-cta">
                  Get Full Analysis →
                </Link>
              </div>

              {/* Quick Actions */}
              <div className="quick-links card">
                <h3>Quick Actions</h3>
                <div className="quick-links-grid">
                  <Link to="/explore" className="quick-link"><Search size={18} /><span>Explore</span></Link>
                  <Link to="/eligibility" className="quick-link"><CheckCircle size={18} /><span>Check</span></Link>
                  <Link to="/assistant" className="quick-link"><Bot size={18} /><span>AI Chat</span></Link>
                  <Link to="/saved" className="quick-link"><Bookmark size={18} /><span>Saved</span></Link>
                </div>
              </div>

            </div>
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

function getMissingFields(user) {
  if (!user) return []
  const fields = { state: 'State', gender: 'Gender', occupation: 'Occupation', education: 'Education', annual_income: 'Income', category: 'Category', date_of_birth: 'Date of Birth' }
  return Object.entries(fields).filter(([k]) => !user[k]).map(([, v]) => v)
}

function getCategoryBreakdown(recommendations) {
  const map = {}
  recommendations.forEach((r) => {
    const cat = r.schemeCategory?.[0] || 'Other'
    map[cat] = (map[cat] || 0) + 1
  })
  const sorted = Object.entries(map).sort((a, b) => b[1] - a[1]).slice(0, 5)
  const max = sorted[0]?.[1] || 1
  return sorted.map(([cat, count]) => ({ cat, count, pct: Math.round((count / max) * 100) }))
}

function getInsights(user, recommendations) {
  const insights = []
  if (!user) return ['Complete your profile to get personalized insights.']
  if (recommendations.length > 0) {
    insights.push(`${recommendations.length} schemes matched your profile.`)
    const topScore = Math.max(...recommendations.map((r) => r.eligibility_score || 0))
    if (topScore > 0) insights.push(`Your top match scores ${Math.round(topScore)}% eligibility.`)
  } else {
    insights.push('Run the eligibility checker to discover schemes tailored for you.')
  }
  if (user.state) insights.push(`Showing schemes for ${user.state} + all Central schemes.`)
  if (user.is_student) insights.push('Student scholarships are prioritized for you.')
  if (user.is_farmer) insights.push('Farmer welfare schemes are included in your matches.')
  return insights.slice(0, 4)
}
