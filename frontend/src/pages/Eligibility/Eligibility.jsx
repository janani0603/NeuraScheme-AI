import { useState } from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../../components/layout/Navbar'
import Sidebar from '../../components/layout/Sidebar'
import BottomNav from '../../components/layout/BottomNav'
import SchemeCard from '../../components/cards/SchemeCard'
import { useAuth } from '../../hooks/useAuth'
import api from '../../services/api'
import './Eligibility.css'

const STATES = ['Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Goa','Gujarat','Haryana','Himachal Pradesh','Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal','Delhi','Jammu & Kashmir','Ladakh','Puducherry']
const OCCUPATIONS = ['Student','Farmer','Government Employee','Private Employee','Self Employed','Business Owner','Unemployed','Homemaker','Retired','Other']
const EDUCATIONS = ['Below 10th','10th Pass','12th Pass','Diploma','Graduate','Post Graduate','PhD','Other']
const CATEGORIES = ['General','OBC','SC','ST','EWS']

const AI_STEPS = [
  { icon: '👤', label: 'Profile Validation', desc: 'Validating and normalizing your profile data' },
  { icon: '🔍', label: 'Scheme Retrieval', desc: 'Searching 3,397 schemes using semantic AI' },
  { icon: '✅', label: 'Eligibility Evaluation', desc: 'Scoring each scheme against your profile' },
  { icon: '🎯', label: 'Recommendation Ranking', desc: 'Ranking schemes by relevance and confidence' },
  { icon: '💡', label: 'Explanation Generation', desc: 'Generating personalized explanations via Gemini AI' },
]

export default function Eligibility() {
  const { user } = useAuth()
  const [step, setStep] = useState(0) // 0=form, 1=loading, 2=results
  const [aiStep, setAiStep] = useState(0)
  const [results, setResults] = useState([])
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    age: '', gender: user?.gender || '', state: user?.state || '',
    occupation: user?.occupation || '', education: user?.education || '',
    annual_income: user?.annual_income || '', category: user?.category || '',
    is_student: user?.is_student || false, is_farmer: user?.is_farmer || false,
    is_business_owner: user?.is_business_owner || false, has_disability: user?.has_disability || false,
  })

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }))

  const runCheck = async () => {
    setError('')
    setStep(1)
    setAiStep(0)

    const payload = { ...form }
    if (payload.annual_income) payload.annual_income = parseFloat(payload.annual_income)
    if (payload.age) payload.age = parseInt(payload.age)

    // Run animation and API call in parallel
    const animateSteps = async () => {
      for (let i = 0; i < AI_STEPS.length; i++) {
        await new Promise((r) => setTimeout(r, 900))
        setAiStep(i + 1)
      }
    }

    const fetchResults = api.post('/ai/recommendations', payload)

    try {
      const [, res] = await Promise.all([animateSteps(), fetchResults])
      setResults(res.data.recommendations || [])
      setStep(2)
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong. Please try again.')
      setStep(0)
    }
  }

  return (
    <div>
      <Navbar />
      <div className="page-layout">
        <Sidebar />
        <main className="page-content">
          <div className="page-title">Eligibility Checker</div>
          <div className="page-subtitle">Fill in your details to get AI-powered scheme recommendations</div>

          {step === 0 && (
            <div className="eligibility-form card">
              <div className="elig-section">
                <h3 className="elig-section-title">Personal Details</h3>
                <div className="elig-grid">
                  <div className="form-group">
                    <label className="form-label">Age</label>
                    <input type="number" className="form-input" placeholder="Your age" value={form.age} onChange={(e) => set('age', e.target.value)} />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Gender</label>
                    <select className="form-select" value={form.gender} onChange={(e) => set('gender', e.target.value)}>
                      <option value="">Select</option>
                      <option>Male</option><option>Female</option><option>Other</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="form-label">State</label>
                    <select className="form-select" value={form.state} onChange={(e) => set('state', e.target.value)}>
                      <option value="">Select State</option>
                      {STATES.map((s) => <option key={s}>{s}</option>)}
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="form-label">Category</label>
                    <select className="form-select" value={form.category} onChange={(e) => set('category', e.target.value)}>
                      <option value="">Select</option>
                      {CATEGORIES.map((c) => <option key={c}>{c}</option>)}
                    </select>
                  </div>
                </div>
              </div>

              <div className="divider" />

              <div className="elig-section">
                <h3 className="elig-section-title">Education & Occupation</h3>
                <div className="elig-grid">
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
                  <div className="form-group">
                    <label className="form-label">Annual Income (₹)</label>
                    <input type="number" className="form-input" placeholder="e.g. 250000" value={form.annual_income} onChange={(e) => set('annual_income', e.target.value)} />
                  </div>
                </div>
              </div>

              <div className="divider" />

              <div className="elig-section">
                <h3 className="elig-section-title">Additional Details</h3>
                <div className="elig-checkboxes">
                  {[['is_student','👨‍🎓 I am a Student'],['is_farmer','🌾 I am a Farmer'],['is_business_owner','💼 I own a Business'],['has_disability','♿ I have a Disability']].map(([k, label]) => (
                    <label key={k} className="elig-checkbox">
                      <input type="checkbox" checked={form[k]} onChange={(e) => set(k, e.target.checked)} />
                      {label}
                    </label>
                  ))}
                </div>
              </div>

              {error && <div className="auth-error">⚠️ {error}</div>}

              <button className="btn btn-primary btn-lg elig-submit" onClick={runCheck}>
                🧠 Run AI Eligibility Check
              </button>
            </div>
          )}

          {step === 1 && (
            <div className="ai-progress card">
              <div className="ai-progress-header">
                <div className="ai-spinner" />
                <div>
                  <h2>AI is analyzing your profile...</h2>
                  <p>Our multi-agent pipeline is working to find the best schemes for you</p>
                </div>
              </div>
              <div className="ai-steps">
                {AI_STEPS.map((s, i) => (
                  <div key={s.label} className={`ai-step ${i < aiStep ? 'done' : i === aiStep ? 'active' : 'pending'}`}>
                    <div className="ai-step-icon">
                      {i < aiStep ? '✅' : i === aiStep ? <span className="ai-step-spinner" /> : '⏳'}
                    </div>
                    <div className="ai-step-content">
                      <div className="ai-step-label">{s.icon} {s.label}</div>
                      <div className="ai-step-desc">{s.desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {step === 2 && (
            <div>
              <div className="results-header">
                <div>
                  <h2>🎯 {results.length} Schemes Found</h2>
                  <p>Ranked by AI eligibility score and semantic relevance</p>
                </div>
                <button className="btn btn-outline" onClick={() => setStep(0)}>← Run Again</button>
              </div>
              {results.length === 0 ? (
                <div className="empty-state card">
                  <div className="empty-icon">😕</div>
                  <h3>No matching schemes found</h3>
                  <p>Try updating your profile with more details for better results.</p>
                </div>
              ) : (
                <div className="schemes-grid">
                  {results.map((r) => <SchemeCard key={r.slug} scheme={r} showScore />)}
                </div>
              )}
            </div>
          )}
        </main>
      </div>
      <BottomNav />
    </div>
  )
}
