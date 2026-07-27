import { useState, useEffect, useCallback } from 'react'
import Navbar from '../../components/layout/Navbar'
import Sidebar from '../../components/layout/Sidebar'
import BottomNav from '../../components/layout/BottomNav'
import SchemeCard from '../../components/cards/SchemeCard'
import { useAuth } from '../../hooks/useAuth'
import api from '../../services/api'
import './Explorer.css'

export default function Explorer() {
  const { isAuthenticated } = useAuth()
  const [schemes, setSchemes] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({ keyword: '', level: '', category: '', sort_by: 'scheme_name', sort_order: 'asc', page: 1 })
  const [total, setTotal] = useState(0)
  const [categories, setCategories] = useState([])

  useEffect(() => {
    api.get('/schemes/filters/categories').then((r) => setCategories(r.data || [])).catch(() => {})
  }, [])

  const fetchSchemes = useCallback(() => {
    setLoading(true)
    const params = { page: filters.page, page_size: 12 }
    if (filters.keyword) params.keyword = filters.keyword
    if (filters.level) params.level = filters.level
    if (filters.category) params.category = filters.category
    if (filters.sort_by) params.sort_by = filters.sort_by
    if (filters.sort_order) params.sort_order = filters.sort_order
    api.get('/schemes', { params })
      .then((r) => { setSchemes(r.data.schemes || []); setTotal(r.data.total || 0) })
      .catch(() => setSchemes([]))
      .finally(() => setLoading(false))
  }, [filters])

  useEffect(() => { fetchSchemes() }, [fetchSchemes])

  const setFilter = (k, v) => setFilters((f) => ({ ...f, [k]: v, page: 1 }))

  const totalPages = Math.ceil(total / 12)
  const hasFilters = filters.level || filters.category || filters.keyword

  const content = (
    <main className={`page-content ${!isAuthenticated ? 'no-sidebar' : ''}`}>
      <div className="page-title">Explore Schemes</div>
      <div className="page-subtitle">Browse {total.toLocaleString()} government schemes</div>

      {/* Search & Filters */}
      <div className="explorer-filters card">
        <div className="search-bar">
          <span className="search-icon">🔍</span>
          <input
            className="search-input"
            placeholder="Search schemes by keyword..."
            value={filters.keyword}
            onChange={(e) => setFilter('keyword', e.target.value)}
          />
          {filters.keyword && (
            <button className="search-clear" onClick={() => setFilter('keyword', '')}>✕</button>
          )}
        </div>
        <div className="filter-row">
          <select className="form-select filter-select" value={filters.level} onChange={(e) => setFilter('level', e.target.value)}>
            <option value="">All Levels</option>
            <option value="Central">Central</option>
            <option value="State">State</option>
          </select>
          <select className="form-select filter-select" value={filters.category} onChange={(e) => setFilter('category', e.target.value)}>
            <option value="">All Categories</option>
            {categories.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
          <select className="form-select filter-select" value={`${filters.sort_by}:${filters.sort_order}`} onChange={(e) => {
            const [sort_by, sort_order] = e.target.value.split(':')
            setFilters((f) => ({ ...f, sort_by, sort_order, page: 1 }))
          }}>
            <option value="scheme_name:asc">A → Z</option>
            <option value="scheme_name:desc">Z → A</option>
            <option value="createdAt:desc">Newest First</option>
            <option value="createdAt:asc">Oldest First</option>
          </select>
          {hasFilters && (
            <button className="btn btn-ghost btn-sm" onClick={() => setFilters({ keyword: '', level: '', category: '', sort_by: 'scheme_name', sort_order: 'asc', page: 1 })}>
              ✕ Clear
            </button>
          )}
        </div>
      </div>

      {/* Results */}
      {loading ? (
        <div className="loading-center"><div className="loading-spinner" /></div>
      ) : schemes.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🔍</div>
          <h3>No schemes found</h3>
          <p>Try different keywords or clear the filters.</p>
        </div>
      ) : (
        <>
          <div className="explorer-results-info">
            Showing {schemes.length} of {total.toLocaleString()} schemes
            {isAuthenticated && <span className="results-hint"> · Login scores shown where available</span>}
          </div>
          <div className="schemes-grid-3">
            {schemes.map((s) => <SchemeCard key={s._id || s.slug} scheme={s} showScore={isAuthenticated} />)}
          </div>
          {totalPages > 1 && (
            <div className="pagination">
              <button className="btn btn-ghost btn-sm" disabled={filters.page === 1} onClick={() => setFilters((f) => ({ ...f, page: f.page - 1 }))}>← Prev</button>
              <span className="page-info">Page {filters.page} of {totalPages}</span>
              <button className="btn btn-ghost btn-sm" disabled={filters.page === totalPages} onClick={() => setFilters((f) => ({ ...f, page: f.page + 1 }))}>Next →</button>
            </div>
          )}
        </>
      )}
    </main>
  )

  return (
    <div>
      <Navbar />
      <div className="page-layout">
        {isAuthenticated && <Sidebar />}
        {content}
      </div>
      {isAuthenticated && <BottomNav />}
    </div>
  )
}
