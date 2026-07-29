import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { Brain, CheckCircle, Lock, Target, Bot, AlertTriangle, Rocket } from 'lucide-react'
import '../Login/Login.css'

const STEPS = ['Account', 'Personal', 'Professional', 'Review']

const STATES = ['Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Goa','Gujarat','Haryana','Himachal Pradesh','Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal','Delhi','Jammu & Kashmir','Ladakh','Puducherry']

const OCCUPATIONS = ['Student','Farmer','Government Employee','Private Employee','Self Employed','Business Owner','Unemployed','Homemaker','Retired','Other']

const EDUCATIONS = ['Below 10th','10th Pass','12th Pass','Diploma','Graduate','Post Graduate','PhD','Other']

const CATEGORIES = ['General','OBC','SC','ST','EWS']

export default function Register() {
  const { register, loading } = useAuth()
  const navigate = useNavigate()
  const [step, setStep] = useState(0)
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    name: '', email: '', phone: '', password: '', confirm_password: '',
    date_of_birth: '', gender: '', state: '', district: '',
    occupation: '', education: '', annual_income: '', category: '',
    is_student: false, is_farmer: false, is_business_owner: false, has_disability: false,
  })

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }))

  const validateStep = () => {
    if (step === 0) {
      if (!form.name || !form.email || !form.password) return 'Please fill all required fields'
      if (form.password !== form.confirm_password) return 'Passwords do not match'
      if (form.password.length < 8) return 'Password must be at least 8 characters'
    }
    if (step === 1) {
      if (!form.gender || !form.state) return 'Please fill all required fields'
    }
    return ''
  }

  const next = () => {
    const err = validateStep()
    if (err) { setError(err); return }
    setError('')
    setStep((s) => s + 1)
  }

  const back = () => { setError(''); setStep((s) => s - 1) }

  const handleSubmit = async () => {
    setError('')
    const payload = { ...form }
    // Convert empty strings to null for optional fields
    const optionalStr = ['phone', 'date_of_birth', 'gender', 'state', 'district', 'occupation', 'education', 'category']
    optionalStr.forEach((k) => { if (payload[k] === '') payload[k] = null })
    payload.annual_income = payload.annual_income ? parseFloat(payload.annual_income) : null
    const res = await register(payload)
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
          <h2>Join thousands of citizens</h2>
          <p>Create your profile once and let AI find the best government schemes for you.</p>
          <div className="auth-features">
            <div className="auth-feature"><CheckCircle size={15} /> Free forever</div>
            <div className="auth-feature"><Lock size={15} /> Your data is secure</div>
            <div className="auth-feature"><Target size={15} /> Personalized results</div>
            <div className="auth-feature"><Bot size={15} /> AI-powered matching</div>
          </div>
        </div>
      </div>

      <div className="auth-right">
        <div className="auth-card card">
          <div className="auth-card-header">
            <h1>Create Account</h1>
            <p>Step {step + 1} of {STEPS.length} — {STEPS[step]}</p>
          </div>

          <div className="step-indicator">
            {STEPS.map((s, i) => (
              <div key={s} style={{ display: 'contents' }}>
                <div className={`step-dot ${i < step ? 'done' : i === step ? 'active' : ''}`}>
                  {i < step ? '✓' : i + 1}
                </div>
                {i < STEPS.length - 1 && <div className={`step-line ${i < step ? 'done' : ''}`} />}
              </div>
            ))}
          </div>

          {error && <div className="auth-error"><AlertTriangle size={15} /> {error}</div>}

          {step === 0 && (
            <div className="auth-form">
              <div className="form-group">
                <label className="form-label">Full Name *</label>
                <input className="form-input" placeholder="Your full name" value={form.name} onChange={(e) => set('name', e.target.value)} />
              </div>
              <div className="form-group">
                <label className="form-label">Email Address *</label>
                <input type="email" className="form-input" placeholder="you@example.com" value={form.email} onChange={(e) => set('email', e.target.value)} />
              </div>
              <div className="form-group">
                <label className="form-label">Phone Number</label>
                <input className="form-input" placeholder="+91 XXXXX XXXXX" value={form.phone} onChange={(e) => set('phone', e.target.value)} />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">Password *</label>
                  <input type="password" className="form-input" placeholder="Min 8 characters" value={form.password} onChange={(e) => set('password', e.target.value)} />
                </div>
                <div className="form-group">
                  <label className="form-label">Confirm Password *</label>
                  <input type="password" className="form-input" placeholder="Repeat password" value={form.confirm_password} onChange={(e) => set('confirm_password', e.target.value)} />
                </div>
              </div>
            </div>
          )}

          {step === 1 && (
            <div className="auth-form">
              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">Date of Birth</label>
                  <input type="date" className="form-input" value={form.date_of_birth} onChange={(e) => set('date_of_birth', e.target.value)} />
                </div>
                <div className="form-group">
                  <label className="form-label">Gender *</label>
                  <select className="form-select" value={form.gender} onChange={(e) => set('gender', e.target.value)}>
                    <option value="">Select</option>
                    <option>Male</option><option>Female</option><option>Other</option>
                  </select>
                </div>
              </div>
              <div className="form-group">
                <label className="form-label">State *</label>
                <select className="form-select" value={form.state} onChange={(e) => set('state', e.target.value)}>
                  <option value="">Select State</option>
                  {STATES.map((s) => <option key={s}>{s}</option>)}
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">District</label>
                <input className="form-input" placeholder="Your district" value={form.district} onChange={(e) => set('district', e.target.value)} />
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="auth-form">
              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">Occupation</label>
                  <select className="form-select" value={form.occupation} onChange={(e) => set('occupation', e.target.value)}>
                    <option value="">Select</option>
                    {OCCUPATIONS.map((o) => <option key={o}>{o}</option>)}
                  </select>
                </div>
                <div className="form-group">
                  <label className="form-label">Education</label>
                  <select className="form-select" value={form.education} onChange={(e) => set('education', e.target.value)}>
                    <option value="">Select</option>
                    {EDUCATIONS.map((e) => <option key={e}>{e}</option>)}
                  </select>
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">Annual Income (₹)</label>
                  <input type="number" className="form-input" placeholder="e.g. 250000" value={form.annual_income} onChange={(e) => set('annual_income', e.target.value)} />
                </div>
                <div className="form-group">
                  <label className="form-label">Category</label>
                  <select className="form-select" value={form.category} onChange={(e) => set('category', e.target.value)}>
                    <option value="">Select</option>
                    {CATEGORIES.map((c) => <option key={c}>{c}</option>)}
                  </select>
                </div>
              </div>
              <div className="checkbox-group">
                {[['is_student','I am a Student'],['is_farmer','I am a Farmer'],['is_business_owner','I own a Business'],['has_disability','I have a Disability']].map(([k, label]) => (
                  <label key={k} className="checkbox-item">
                    <input type="checkbox" checked={form[k]} onChange={(e) => set(k, e.target.checked)} />
                    {label}
                  </label>
                ))}
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="auth-form">
              <div className="review-section">
                <h4>Account</h4>
                <div className="review-grid">
                  <div className="review-item"><span>Name</span><span>{form.name || '—'}</span></div>
                  <div className="review-item"><span>Email</span><span>{form.email || '—'}</span></div>
                </div>
              </div>
              <div className="divider" />
              <div className="review-section">
                <h4>Personal</h4>
                <div className="review-grid">
                  <div className="review-item"><span>Gender</span><span>{form.gender || '—'}</span></div>
                  <div className="review-item"><span>State</span><span>{form.state || '—'}</span></div>
                  <div className="review-item"><span>DOB</span><span>{form.date_of_birth || '—'}</span></div>
                  <div className="review-item"><span>District</span><span>{form.district || '—'}</span></div>
                </div>
              </div>
              <div className="divider" />
              <div className="review-section">
                <h4>Professional</h4>
                <div className="review-grid">
                  <div className="review-item"><span>Occupation</span><span>{form.occupation || '—'}</span></div>
                  <div className="review-item"><span>Education</span><span>{form.education || '—'}</span></div>
                  <div className="review-item"><span>Income</span><span>{form.annual_income ? `₹${Number(form.annual_income).toLocaleString()}` : '—'}</span></div>
                  <div className="review-item"><span>Category</span><span>{form.category || '—'}</span></div>
                </div>
              </div>
            </div>
          )}

          <div className="step-actions" style={{ marginTop: 20 }}>
            {step > 0 && <button className="btn btn-ghost" onClick={back}>← Back</button>}
            {step < 3
              ? <button className="btn btn-primary" style={{ flex: 1, justifyContent: 'center' }} onClick={next}>Continue →</button>
              : <button className="btn btn-primary" style={{ flex: 1, justifyContent: 'center' }} onClick={handleSubmit} disabled={loading}>
                  {loading ? 'Creating Account...' : <><Rocket size={15} /> Create Account</>}
                </button>
            }
          </div>

          <p className="auth-switch">
            Already have an account? <Link to="/login">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
