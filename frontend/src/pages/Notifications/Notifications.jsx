import Navbar from '../../components/layout/Navbar'
import Sidebar from '../../components/layout/Sidebar'
import BottomNav from '../../components/layout/BottomNav'
import './Notifications.css'

export default function Notifications() {
  return (
    <div>
      <Navbar />
      <div className="page-layout">
        <Sidebar />
        <main className="page-content">
          <div className="page-title">Notifications</div>
          <div className="page-subtitle">Stay updated on schemes and deadlines</div>

          <div className="empty-state card">
            <div className="empty-icon">🔔</div>
            <h3>No notifications yet</h3>
            <p>You'll be notified about new schemes, deadlines, and updates here.</p>
          </div>
        </main>
      </div>
      <BottomNav />
    </div>
  )
}
