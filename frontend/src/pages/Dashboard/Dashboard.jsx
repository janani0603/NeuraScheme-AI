import { useState, useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../../components/layout/Navbar'
import Sidebar from '../../components/layout/Sidebar'
import BottomNav from '../../components/layout/BottomNav'
import SchemeCard from '../../components/cards/SchemeCard'
import { useAuth } from '../../hooks/useAuth'
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

  const stats = [
    { icon: '🎯', label: 'Eligible Schemes', value: recommendations.length || '—', color: 'blue' },
    { icon: '❤️', label: 'Saved Schemes', value: user?.saved_schemes?.length || 0, color: 'red' },
    { icon: '✅', label: 'Profile Complete', value: completeness + '%', color: 'green' },
    { icon: '🔔', label: 'Notifications', value: '0', color: 'yellow' },
  ]

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
              <h1>{greeting}, {user?.name?.split(' ')[0] || 'there'} 👋</h1>
              <p>Here's your personalized government scheme dashboard.</p>
            </div>
            <div className="welcome-actions">
              <Link to="/eligibility" className="btn btn-primary">🧠 Run AI Check</Link>
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

          {/* Profile nudge */}
          {completeness < 100 && (
            <div className="profile-nudge card">
              <div className="nudge-content">
                <span className="nudge-icon">📝</span>
                <div>
                  <strong>Complete your profile ({completeness}% done)</strong>
                  <p>A complete profile gives you more accurate AI recommendations.</p>
                </div>
              </div>
              <Link to="/profile" className="btn btn-primary btn-sm">Complete Profile</Link>
            </div>
          )}

          <div className="dashboard-two-col">
            {/* Recommendations */}
            <div className="dashboard-section">
              <div className="section-title-row">
                <h2>Your Recommendations</h2>
                <Link to="/eligibility" className="btn btn-outline btn-sm">↻ Refresh</Link>
              </div>

              {loading ? (
                <div className="loading-center"><div className="loading-spinner" /></div>
              ) : recommendations.length === 0 ? (
                <div className="empty-state card">
                  <div className="empty-icon">🎯</div>
                  <h3>No recommendations yet</h3>
                  <p>Run the eligibility checker to get AI-powered scheme recommendations.</p>
                  <Link to="/eligibility" className="btn btn-primary" style={{ marginTop: 16 }}>Check Eligibility</Link>
                </div>
              ) : (
                <div className="schemes-grid">
                  {recommendations.slice(0, 6).map((r) => (
                    <SchemeCard key={r._id || r.slug} scheme={r} showScore />
                  ))}
                </div>
              )}
            </div>

            {/* Right column */}
            <div className="dashboard-right">

              {/* AI Insights */}
              <div className="ai-insights card">
                <div className="insights-header">
                  <span className="insights-icon">🧠</span>
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

              {/* Notifications Panel */}
              <div className="notif-panel card">
                <div className="insights-header">
                  <span className="insights-icon">🔔</span>
                  <h3>Notifications</h3>
                </div>
                <div className="notif-empty">
                  <p>No new notifications</p>
                  <span>You'll be notified about deadlines and new schemes here.</span>
                </div>
              </div>

              {/* Quick Links */}
              <div className="quick-links card">
                <h3>Quick Actions</h3>
                <div className="quick-links-grid">
                  <Link to="/explore" className="quick-link">🔍<span>Explore</span></Link>
                  <Link to="/eligibility" className="quick-link">✅<span>Check</span></Link>
                  <Link to="/assistant" className="quick-link">🤖<span>AI Chat</span></Link>
                  <Link to="/saved" className="quick-link">❤️<span>Saved</span></Link>
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

function getInsights(user, recommendations) {
  const insights = []
  if (!user) return ['Complete your profile to get personalized insights.']
  if (recommendations.length > 0) {
    insights.push(`Based on your profile, ${recommendations.length} schemes match your eligibility.`)
    const topScore = Math.max(...recommendations.map((r) => r.eligibility_score || 0))
    if (topScore > 0) insights.push(`Your top match has an eligibility score of ${Math.round(topScore)}%.`)
  } else {
    insights.push('Run the eligibility checker to discover schemes tailored for you.')
  }
  if (user.state) insights.push(`Showing schemes available in ${user.state} and Central schemes.`)
  if (user.is_student) insights.push('Student-specific scholarships and education schemes are prioritized for you.')
  if (user.is_farmer) insights.push('Agricultural and farmer welfare schemes are included in your recommendations.')
  if (insights.length === 0) insights.push('Complete your profile to get personalized AI insights.')
  return insights.slice(0, 4)
}
