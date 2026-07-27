import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../../components/layout/Navbar'
import Sidebar from '../../components/layout/Sidebar'
import BottomNav from '../../components/layout/BottomNav'
import SchemeCard from '../../components/cards/SchemeCard'
import api from '../../services/api'
import './Saved.css'

export default function Saved() {
  const [schemes, setSchemes] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/users/me/saved')
      .then((r) => setSchemes(r.data || []))
      .catch(() => setSchemes([]))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div>
      <Navbar />
      <div className="page-layout">
        <Sidebar />
        <main className="page-content">
          <div className="page-title">Saved Schemes</div>
          <div className="page-subtitle">Schemes you've bookmarked for later</div>

          {loading ? (
            <div className="loading-center"><div className="loading-spinner" /></div>
          ) : schemes.length === 0 ? (
            <div className="empty-state card">
              <div className="empty-icon">❤️</div>
              <h3>No saved schemes yet</h3>
              <p>Browse schemes and save the ones you're interested in.</p>
              <Link to="/explore" className="btn btn-primary" style={{ marginTop: 16 }}>Explore Schemes</Link>
            </div>
          ) : (
            <>
              <div className="saved-count">{schemes.length} saved scheme{schemes.length !== 1 ? 's' : ''}</div>
              <div className="schemes-grid-2">
                {schemes.map((s) => <SchemeCard key={s.slug} scheme={s} />)}
              </div>
            </>
          )}
        </main>
      </div>
      <BottomNav />
    </div>
  )
}
