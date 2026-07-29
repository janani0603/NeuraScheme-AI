import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { Brain, CheckCircle, Bot, Target, FileText, Eye, EyeOff, AlertTriangle } from 'lucide-react'
import './Login.css'

export default function Login() {
  const { login, loading } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [showPass, setShowPass] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    const res = await login(form.email, form.password)
    if (res.success) navigate('/dashboard')
    else setError(res.error)
  }

  return (
    <div className="auth-page">
      <div className="auth-left">
        <Link to="/" className="auth-brand">
          <Brain size={20} /> NeuraScheme <strong>AI</strong>
        </Link>
        <div className="auth-left-content">
          <h2>Discover schemes made for you</h2>
          <p>AI-powered recommendations based on your profile, location, and eligibility.</p>
          <div className="auth-features">
            <div className="auth-feature"><CheckCircle size={15} /> 3,397 Government Schemes</div>
            <div className="auth-feature"><Bot size={15} /> Multi-Agent AI Pipeline</div>
            <div className="auth-feature"><Target size={15} /> Personalized Recommendations</div>
            <div className="auth-feature"><FileText size={15} /> Document Guidance</div>
          </div>
        </div>
      </div>

      <div className="auth-right">
        <div className="auth-card card">
          <div className="auth-card-header">
            <h1>Welcome back</h1>
            <p>Sign in to your NeuraScheme AI account</p>
          </div>

          {error && <div className="auth-error"><AlertTriangle size={15} /> {error}</div>}

          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group">
              <label className="form-label">Email Address</label>
              <input
                type="email"
                className="form-input"
                placeholder="you@example.com"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Password</label>
              <div className="input-with-icon">
                <input
                  type={showPass ? 'text' : 'password'}
                  className="form-input"
                  placeholder="Enter your password"
                  value={form.password}
                  onChange={(e) => setForm({ ...form, password: e.target.value })}
                  required
                />
                <button type="button" className="input-icon-btn" onClick={() => setShowPass(!showPass)}>
                  {showPass ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            <button type="submit" className="btn btn-primary btn-lg auth-submit" disabled={loading}>
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <p className="auth-switch">
            Don't have an account? <Link to="/register">Create one free</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
