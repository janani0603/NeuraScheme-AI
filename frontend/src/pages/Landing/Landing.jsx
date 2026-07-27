import { useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../../components/layout/Navbar'
import './Landing.css'

const testimonials = [
  { name: 'Ramesh Kumar', state: 'Uttar Pradesh', text: 'Found PM Kisan and 3 other schemes I never knew existed. Got ₹6,000 in my account within a month!', role: 'Farmer' },
  { name: 'Priya Sharma', state: 'Maharashtra', text: 'The AI matched me with a scholarship that covered my entire college fee. Absolutely life-changing.', role: 'Student' },
  { name: 'Suresh Patel', state: 'Gujarat', text: 'As a small business owner, I found MUDRA loan scheme through NeuraScheme. The document checklist saved me so much time.', role: 'Business Owner' },
]

const trustLogos = ['🏛️ Ministry of Finance', '🌾 PM Kisan', '🎓 NSP Scholarships', '🏠 PM Awas', '💊 Ayushman Bharat', '⚡ PM KUSUM']

const features = [
  { icon: '🔍', title: 'Smart Search', desc: 'Search thousands of schemes by keyword, category, state, or occupation.' },
  { icon: '🎯', title: 'Personalized Recommendations', desc: 'AI-powered recommendations tailored to your profile and eligibility.' },
  { icon: '✅', title: 'Eligibility Checker', desc: 'Instantly know which schemes you qualify for with detailed scoring.' },
  { icon: '🤖', title: 'AI Assistant', desc: 'Ask questions about any scheme and get instant, grounded answers.' },
  { icon: '📄', title: 'Document Guidance', desc: 'Know exactly which documents you need for each scheme.' },
  { icon: '🔔', title: 'Deadline Alerts', desc: 'Never miss an application deadline with smart notifications.' },
]

const steps = [
  { icon: '👤', title: 'Create Profile', desc: 'Tell us about yourself — state, occupation, income, education.' },
  { icon: '🧠', title: 'AI Analysis', desc: 'Our multi-agent AI analyzes thousands of schemes for you.' },
  { icon: '✅', title: 'Eligibility Check', desc: 'Each scheme is scored against your profile automatically.' },
  { icon: '🎯', title: 'Get Recommendations', desc: 'Receive a ranked list of schemes best suited for you.' },
  { icon: '📋', title: 'Apply with Guidance', desc: 'Follow step-by-step instructions with document checklists.' },
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

export default function Landing() {
  const ref3397 = useCountUp(3397)
  const ref28 = useCountUp(28)
  const ref6 = useCountUp(6)
  return (
    <div className="landing">
      <Navbar />

      {/* Hero */}
      <section className="hero-section">
        <div className="container hero-container">
          <div className="hero-content">
            <div className="hero-badge">🇮🇳 3,000+ Government Schemes</div>
            <h1 className="hero-title">
              Find the Right Government Scheme <span>in Minutes</span>
            </h1>
            <p className="hero-subtitle">
              Discover personalized government schemes using AI-powered recommendations,
              eligibility analysis, and intelligent guidance — all in one place.
            </p>
            <div className="hero-actions">
              <Link to="/register" className="btn btn-primary btn-lg">Get Started Free</Link>
              <Link to="/explore" className="btn btn-outline btn-lg">Explore Schemes</Link>
            </div>
            <div className="hero-stats">
              <div className="hero-stat"><strong ref={ref3397}>3,397</strong><span>Schemes</span></div>
              <div className="hero-stat-divider" />
              <div className="hero-stat"><strong ref={ref28}>28</strong><span>States</span></div>
              <div className="hero-stat-divider" />
              <div className="hero-stat"><strong ref={ref6}>6</strong><span>AI Agents</span></div>
              <div className="hero-stat-divider" />
              <div className="hero-stat"><strong>Free</strong><span>Forever</span></div>
            </div>
          </div>
          <div className="hero-visual">
            <div className="hero-card-stack">
              <div className="hero-card hero-card-1">
                <div className="hc-icon">🎓</div>
                <div>
                  <div className="hc-title">National Scholarship</div>
                  <div className="hc-score">Match: 96%</div>
                </div>
              </div>
              <div className="hero-card hero-card-2">
                <div className="hc-icon">🌾</div>
                <div>
                  <div className="hc-title">PM Kisan Yojana</div>
                  <div className="hc-score">Match: 88%</div>
                </div>
              </div>
              <div className="hero-card hero-card-3">
                <div className="hc-icon">🏠</div>
                <div>
                  <div className="hc-title">PM Awas Yojana</div>
                  <div className="hc-score">Match: 74%</div>
                </div>
              </div>
              <div className="hero-ai-badge">🧠 AI Powered</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="features-section" id="features">
        <div className="container">
          <div className="section-header">
            <h2>Everything You Need</h2>
            <p>Powerful tools to help you discover and apply for government schemes</p>
          </div>
          <div className="features-grid">
            {features.map((f) => (
              <div key={f.title} className="feature-card card">
                <div className="feature-icon">{f.icon}</div>
                <h3>{f.title}</h3>
                <p>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Trust Bar */}
      <section className="trust-section">
        <div className="container">
          <p className="trust-label">Covering schemes from</p>
          <div className="trust-logos">
            {trustLogos.map((l) => (
              <div key={l} className="trust-logo">{l}</div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="how-section" id="about">
        <div className="container">
          <div className="section-header">
            <h2>How It Works</h2>
            <p>From profile to recommendations in under a minute</p>
          </div>
          <div className="steps-list">
            {steps.map((step, i) => (
              <div key={step.title} className="step-item">
                <div className="step-number">{i + 1}</div>
                <div className="step-icon">{step.icon}</div>
                <div className="step-content">
                  <h3>{step.title}</h3>
                  <p>{step.desc}</p>
                </div>
                {i < steps.length - 1 && <div className="step-arrow">→</div>}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="testimonials-section">
        <div className="container">
          <div className="section-header">
            <h2>Real People, Real Impact</h2>
            <p>Citizens across India are discovering schemes they never knew existed</p>
          </div>
          <div className="testimonials-grid">
            {testimonials.map((t) => (
              <div key={t.name} className="testimonial-card card">
                <div className="testimonial-stars">★★★★★</div>
                <p className="testimonial-text">&ldquo;{t.text}&rdquo;</p>
                <div className="testimonial-author">
                  <div className="testimonial-avatar">{t.name[0]}</div>
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
          <div className="cta-box">
            <h2>Start Discovering Schemes Today</h2>
            <p>Join thousands of citizens who found the right government support through NeuraScheme AI.</p>
            <div className="cta-actions">
              <Link to="/register" className="btn btn-primary btn-lg">Create Free Account</Link>
              <Link to="/explore" className="btn btn-outline btn-lg">Browse Schemes</Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="container footer-inner">
          <div className="footer-brand">
            <span>🧠</span>
            <span>NeuraScheme <strong>AI</strong></span>
          </div>
          <p className="footer-copy">© 2025 NeuraScheme AI. Making Government Schemes Accessible.</p>
          <div className="footer-links">
            <a href="#">Privacy</a>
            <a href="#">Terms</a>
            <a href="#">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  )
}
