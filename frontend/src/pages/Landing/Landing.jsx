import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../../components/layout/Navbar'
import {
  Search, Target, CheckCircle, Bot, FileText, Bell,
  User, Brain, ClipboardList, GraduationCap, Wheat,
  Home, HeartPulse, Zap, Building2, Baby, Factory,
  Rocket, Lightbulb, ArrowRight
} from 'lucide-react'
import './Landing.css'

const testimonials = [
  { name: 'Ramesh Kumar', state: 'Uttar Pradesh', text: 'Found PM Kisan and 3 other schemes I never knew existed. Got ₹6,000 in my account within a month!', role: 'Farmer', avatar: 'R' },
  { name: 'Priya Sharma', state: 'Maharashtra', text: 'The AI matched me with a scholarship that covered my entire college fee. Absolutely life-changing.', role: 'Student', avatar: 'P' },
  { name: 'Suresh Patel', state: 'Gujarat', text: 'Found MUDRA loan scheme through NeuraScheme. The document checklist saved me so much time.', role: 'Business Owner', avatar: 'S' },
]

const trustLogos = [
  { icon: Building2, label: 'Ministry of Finance' },
  { icon: Wheat, label: 'PM Kisan' },
  { icon: GraduationCap, label: 'NSP Scholarships' },
  { icon: Home, label: 'PM Awas Yojana' },
  { icon: HeartPulse, label: 'Ayushman Bharat' },
  { icon: Zap, label: 'PM KUSUM' },
  { icon: Baby, label: 'Beti Bachao' },
  { icon: Factory, label: 'Make in India' },
]

const features = [
  { icon: Search, title: 'Smart Search', desc: 'Search thousands of schemes by keyword, category, state, or occupation in seconds.', color: '#1A4FA0' },
  { icon: Target, title: 'AI Recommendations', desc: 'Multi-agent AI analyzes your profile and ranks schemes by eligibility score.', color: '#7C3AED' },
  { icon: CheckCircle, title: 'Eligibility Checker', desc: 'Instantly know which schemes you qualify for with detailed condition scoring.', color: '#059669' },
  { icon: Bot, title: 'AI Assistant', desc: 'Ask anything about any scheme and get instant, grounded answers.', color: '#DC2626' },
  { icon: FileText, title: 'Document Guidance', desc: 'Know exactly which documents you need before you start applying.', color: '#D97706' },
  { icon: Bell, title: 'Deadline Alerts', desc: 'Never miss an application deadline with smart notifications.', color: '#0891B2' },
]

const steps = [
  {
    number: '01',
    icon: User,
    title: 'Create Your Profile',
    desc: 'Tell us about yourself — your state, occupation, income, education, and category. Takes less than 2 minutes.',
    detail: 'Your data is secure and used only to match you with relevant schemes.',
    color: '#1A4FA0',
  },
  {
    number: '02',
    icon: Brain,
    title: 'AI Analyzes Schemes',
    desc: 'Our 9-agent AI pipeline scans 3,397 government schemes and scores each one against your profile.',
    detail: 'Uses semantic search + rule-based eligibility engine for accuracy.',
    color: '#7C3AED',
  },
  {
    number: '03',
    icon: CheckCircle,
    title: 'Eligibility Scoring',
    desc: 'Each scheme gets a personalized eligibility score based on state, income, occupation, category, and more.',
    detail: 'Matched and missing conditions are clearly shown for every scheme.',
    color: '#059669',
  },
  {
    number: '04',
    icon: Target,
    title: 'Get Ranked Results',
    desc: 'Receive a ranked list of schemes best suited for you, sorted by how well you qualify.',
    detail: 'Top matches include AI-written personalized explanations.',
    color: '#D97706',
  },
  {
    number: '05',
    icon: ClipboardList,
    title: 'Apply with Guidance',
    desc: 'Follow step-by-step application instructions with document checklists for each scheme.',
    detail: 'Ask the AI assistant any question about the scheme before applying.',
    color: '#DC2626',
  },
]

const stats = [
  { value: 3397, label: 'Government Schemes', suffix: '+' },
  { value: 28, label: 'States Covered', suffix: '+' },
  { value: 9, label: 'AI Agents', suffix: '' },
  { value: 100, label: 'Free Forever', suffix: '%' },
]

// Phone mock card data
const phoneCards = [
  { icon: GraduationCap, name: 'National Scholarship', cat: 'Education · Central', score: '96%', scoreClass: 'pc-score-high', active: true },
  { icon: Wheat, name: 'PM Kisan Yojana', cat: 'Agriculture · Central', score: '88%', scoreClass: 'pc-score-high', active: false },
  { icon: Home, name: 'PM Awas Yojana', cat: 'Housing · Central', score: '74%', scoreClass: 'pc-score-med', active: false },
  { icon: HeartPulse, name: 'Ayushman Bharat', cat: 'Health · Central', score: '68%', scoreClass: 'pc-score-med', active: false },
]

function useCountUp(target, duration = 1800) {
  const ref = useRef(null)
  useEffect(() => {
    const el = ref.current
    if (!el) return
    const observer = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return
      observer.disconnect()
      let start = 0
      const step = (timestamp) => {
        if (!start) start = timestamp
        const progress = Math.min((timestamp - start) / duration, 1)
        el.textContent = Math.floor(progress * target).toLocaleString()
        if (progress < 1) requestAnimationFrame(step)
        else el.textContent = target.toLocaleString()
      }
      requestAnimationFrame(step)
    }, { threshold: 0.5 })
    observer.observe(el)
    return () => observer.disconnect()
  }, [target, duration])
  return ref
}

function useScrollReveal() {
  useEffect(() => {
    const els = document.querySelectorAll('.reveal')
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed')
          observer.unobserve(entry.target)
        }
      })
    }, { threshold: 0.12 })
    els.forEach((el) => observer.observe(el))
    return () => observer.disconnect()
  }, [])
}

export default function Landing() {
  const ref3397 = useCountUp(3397)
  const ref28 = useCountUp(28)
  const ref6 = useCountUp(6)
  const [activeStep, setActiveStep] = useState(0)
  useScrollReveal()

  return (
    <div className="landing">
      <Navbar />

      {/* Hero */}
      <section className="hero-section">
        <div className="hero-bg-orb hero-orb-1" />
        <div className="hero-bg-orb hero-orb-2" />
        <div className="hero-bg-orb hero-orb-3" />
        <div className="container hero-container">
          <div className="hero-content">
            <div className="hero-badge">
              <span className="hero-badge-dot" />
              India's Smartest Scheme Discovery Platform
            </div>
            <h1 className="hero-title">
              Find Government Schemes<br />
              <span className="hero-title-gradient">Made Just for You</span>
            </h1>
            <p className="hero-subtitle">
              AI-powered eligibility matching across 3,397 central and state schemes.
              Know what you qualify for, what documents you need, and how to apply — in minutes.
            </p>
            <div className="hero-actions">
              <Link to="/register" className="btn btn-primary btn-lg hero-cta-primary">
                <Rocket size={16} /> Get Started Free
              </Link>
              <Link to="/explore" className="btn btn-outline btn-lg">
                Browse Schemes <ArrowRight size={15} />
              </Link>
            </div>
            <div className="hero-stats">
              <div className="hero-stat">
                <strong ref={ref3397}>3,397</strong>
                <span>Schemes</span>
              </div>
              <div className="hero-stat-divider" />
              <div className="hero-stat">
                <strong ref={ref28}>28</strong>
                <span>States</span>
              </div>
              <div className="hero-stat-divider" />
              <div className="hero-stat">
                <strong ref={ref6}>9</strong>
                <span>AI Agents</span>
              </div>
              <div className="hero-stat-divider" />
              <div className="hero-stat">
                <strong>Free</strong>
                <span>Forever</span>
              </div>
            </div>
          </div>

          <div className="hero-visual">
            <div className="hero-phone-mockup">
              <div className="phone-header">
                <div className="phone-dot" /><div className="phone-dot" /><div className="phone-dot" />
              </div>
              <div className="phone-title"><Brain size={14} /> AI Recommendations</div>
              <div className="phone-cards">
                {phoneCards.map((c) => {
                  const CardIcon = c.icon
                  return (
                    <div key={c.name} className={`phone-card ${c.active ? 'phone-card-active' : ''}`}>
                      <div className="pc-left">
                        <div className="pc-icon"><CardIcon size={16} /></div>
                        <div>
                          <div className="pc-name">{c.name}</div>
                          <div className="pc-cat">{c.cat}</div>
                        </div>
                      </div>
                      <div className={`pc-score ${c.scoreClass}`}>{c.score}</div>
                    </div>
                  )
                })}
              </div>
              <div className="phone-footer">
                <span><CheckCircle size={12} /> 4 schemes matched</span>
                <span className="phone-ai-tag"><Brain size={12} /> AI Powered</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Bar */}
      <section className="trust-section">
        <div className="container">
          <p className="trust-label">Covering schemes from</p>
          <div className="trust-track">
            <div className="trust-logos">
              {[...trustLogos, ...trustLogos].map((l, i) => {
                const TrustIcon = l.icon
                return (
                  <div key={i} className="trust-logo">
                    <TrustIcon size={15} /> {l.label}
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="features-section" id="features">
        <div className="container">
          <div className="section-header reveal">
            <div className="section-tag">Features</div>
            <h2>Everything You Need to Find the Right Scheme</h2>
            <p>Powerful AI tools that make government schemes accessible to every citizen</p>
          </div>
          <div className="features-grid">
            {features.map((f, i) => {
              const FIcon = f.icon
              return (
                <div key={f.title} className="feature-card card reveal" style={{ animationDelay: `${i * 0.08}s` }}>
                  <div className="feature-icon-wrap" style={{ background: f.color + '15', color: f.color }}>
                    <FIcon size={22} />
                  </div>
                  <h3>{f.title}</h3>
                  <p>{f.desc}</p>
                  <div className="feature-arrow" style={{ color: f.color }}><ArrowRight size={16} /></div>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="how-section" id="about">
        <div className="container">
          <div className="section-header reveal">
            <div className="section-tag">How It Works</div>
            <h2>From Profile to Recommendations in 60 Seconds</h2>
            <p>Our AI pipeline does the heavy lifting so you don't have to</p>
          </div>

          <div className="how-layout">
            <div className="steps-nav">
              {steps.map((step, i) => (
                <button
                  key={step.number}
                  className={`step-nav-item ${activeStep === i ? 'active' : ''}`}
                  onClick={() => setActiveStep(i)}
                  style={{ '--step-color': step.color }}
                >
                  <div className="step-nav-number">{step.number}</div>
                  <div className="step-nav-text">
                    <div className="step-nav-title">{step.title}</div>
                  </div>
                  <div className="step-nav-indicator" />
                </button>
              ))}
            </div>

            <div className="step-detail-panel">
              {steps.map((step, i) => {
                const StepIcon = step.icon
                return (
                  <div key={step.number} className={`step-detail ${activeStep === i ? 'active' : ''}`}>
                    <div className="step-detail-icon" style={{ background: step.color + '15', color: step.color }}>
                      <StepIcon size={28} />
                    </div>
                    <div className="step-detail-number" style={{ color: step.color }}>{step.number}</div>
                    <h3 className="step-detail-title">{step.title}</h3>
                    <p className="step-detail-desc">{step.desc}</p>
                    <div className="step-detail-note">
                      <span className="step-note-icon"><Lightbulb size={14} /></span>
                      {step.detail}
                    </div>
                    <div className="step-detail-progress">
                      {steps.map((_, j) => (
                        <div
                          key={j}
                          className={`progress-dot ${j === i ? 'active' : j < i ? 'done' : ''}`}
                          onClick={() => setActiveStep(j)}
                        />
                      ))}
                    </div>
                    <div className="step-detail-actions">
                      {i > 0 && (
                        <button className="btn btn-ghost btn-sm" onClick={() => setActiveStep(i - 1)}>← Prev</button>
                      )}
                      {i < steps.length - 1 ? (
                        <button className="btn btn-primary btn-sm" onClick={() => setActiveStep(i + 1)} style={{ marginLeft: 'auto' }}>Next →</button>
                      ) : (
                        <Link to="/register" className="btn btn-primary btn-sm" style={{ marginLeft: 'auto' }}>Get Started →</Link>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Mobile steps */}
          <div className="steps-mobile">
            {steps.map((step, i) => {
              const StepIcon = step.icon
              return (
                <div key={step.number} className="step-mobile-item reveal">
                  <div className="step-mobile-left">
                    <div className="step-mobile-circle" style={{ background: step.color }}>
                      {step.number}
                    </div>
                    {i < steps.length - 1 && <div className="step-mobile-line" />}
                  </div>
                  <div className="step-mobile-content">
                    <div className="step-mobile-icon"><StepIcon size={20} /></div>
                    <h3>{step.title}</h3>
                    <p>{step.desc}</p>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Stats Banner */}
      <section className="stats-section reveal">
        <div className="container">
          <div className="stats-grid">
            {stats.map((s) => (
              <div key={s.label} className="stats-item">
                <div className="stats-value">{s.value.toLocaleString()}{s.suffix}</div>
                <div className="stats-label">{s.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="testimonials-section">
        <div className="container">
          <div className="section-header reveal">
            <div className="section-tag">Testimonials</div>
            <h2>Real People, Real Impact</h2>
            <p>Citizens across India are discovering schemes they never knew existed</p>
          </div>
          <div className="testimonials-grid">
            {testimonials.map((t, i) => (
              <div key={t.name} className="testimonial-card card reveal" style={{ animationDelay: `${i * 0.1}s` }}>
                <div className="testimonial-quote">"</div>
                <div className="testimonial-stars">★★★★★</div>
                <p className="testimonial-text">{t.text}</p>
                <div className="testimonial-author">
                  <div className="testimonial-avatar">{t.avatar}</div>
                  <div>
                    <div className="testimonial-name">{t.name}</div>
                    <div className="testimonial-meta">{t.role} · {t.state}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-box reveal">
            <div className="cta-orb cta-orb-1" />
            <div className="cta-orb cta-orb-2" />
            <div className="cta-badge"><Rocket size={13} /> Free · No Credit Card · Instant Access</div>
            <h2>Start Discovering Schemes Today</h2>
            <p>Join thousands of citizens who found the right government support through NeuraScheme AI.</p>
            <div className="cta-actions">
              <Link to="/register" className="btn btn-primary btn-lg cta-btn-white">Create Free Account</Link>
              <Link to="/explore" className="btn btn-outline btn-lg cta-btn-outline">Browse Schemes</Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="container">
          <div className="footer-top">
            <div className="footer-brand-col">
              <div className="footer-brand">
                <Brain size={20} />
                <span>NeuraScheme <strong>AI</strong></span>
              </div>
              <p className="footer-tagline">Making Government Schemes Accessible to Every Indian Citizen.</p>
            </div>
            <div className="footer-links-col">
              <div className="footer-link-group">
                <div className="footer-link-title">Platform</div>
                <Link to="/explore">Explore Schemes</Link>
                <Link to="/register">Get Started</Link>
                <Link to="/login">Sign In</Link>
              </div>
              <div className="footer-link-group">
                <div className="footer-link-title">Company</div>
                <a href="#features">Features</a>
                <a href="#about">How It Works</a>
                <a href="#">Contact</a>
              </div>
              <div className="footer-link-group">
                <div className="footer-link-title">Legal</div>
                <a href="#">Privacy Policy</a>
                <a href="#">Terms of Service</a>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>© 2026 NeuraScheme AI. All rights reserved.</p>
            <p>Built for India</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
