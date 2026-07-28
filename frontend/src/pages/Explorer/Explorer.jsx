import { useState, useEffect, useCallback, useRef } from 'react'
import Navbar from '../../components/layout/Navbar'
import Sidebar from '../../components/layout/Sidebar'
import BottomNav from '../../components/layout/BottomNav'
import SchemeCard from '../../components/cards/SchemeCard'
import { useAuth } from '../../hooks/useAuth'
import api from '../../services/api'
import './Explorer.css'

const INDIAN_STATES = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
  'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
  'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
  'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
  'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
  'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra and Nagar Haveli',
  'Daman and Diu', 'Delhi', 'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry',
]

const INITIAL_FILTERS = {
  keyword: '', level: '', category: '', tag: '', state: '',
  sort_by: 'scheme_name', sort_order: 'asc', page: 1,
}

export default function Explorer() {
  const { isAuthenticated } = useAuth()
  const [schemes, setSchemes] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState(INITIAL_FILTERS)
  const [searchInput, setSearchInput] = useState('')
  const [total, setTotal] = useState(0)
  const [categories, setCategories] = useState([])
  const [tags, setTags] = useState([])
  const debounceRef = useRef(null)

  useEffect(() => {
    api.get('/schemes/filters/categories').then((r) => setCategories(r.data || [])).catch(() => {})
    api.get('/schemes/filters/tags').then((r) => setTags((r.data || []).slice(0, 30))).catch(() => {})
  }, [])

  // Debounce keyword search
  useEffect(() => {
    clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => {
      setFilters((f) => ({ ...f, keyword: searchInput, page: 1 }))
    }, 400)
    return () => clearTimeout(debounceRef.current)
  }, [searchInput])

  const fetchSchemes = useCallback(() => {
    setLoading(true)
    const params = { page: filters.page, page_size: 12 }
    if (filters.keyword) params.keyword = filters.keyword
    if (filters.level) params.level = filters.level
    if (filters.category) params.category = filters.category
    if (filters.tag) params.tag = filters.tag
    if (filters.state) params.state = filters.state
    if (filters.sort_by) params.sort_by = filters.sort_by
    if (filters.sort_order) params.sort_order = filters.sort_order
    api.get('/schemes', { params })
      .then((r) => { setSchemes(r.data.schemes || []); setTotal(r.data.total || 0) })
      .catch(() => setSchemes([]))
      .finally(() => setLoading(false))
  }, [filters])

  useEffect(() => { fetchSchemes() }, [fetchSchemes])

  const setFilter = (k, v) => setFilters((f) => ({ ...f, [k]: v, page: 1 }))

  const clearAll = () => {
    setSearchInput('')
    setFilters(INITIAL_FILTERS)
  }

  const totalPages = Math.ceil(total / 12)

  // Active filter badges
  const activeFilters = [
    filters.level && { key: 'level', label: `Level: ${filters.level}` },
    filters.category && { key: 'category', label: `Category: ${filters.category}` },
    filters.state && { key: 'state', label: `State: ${filters.state}` },
    filters.tag && { key: 'tag', label: `Tag: ${filters.tag}` },
  ].filter(Boolean)

  const hasFilters = activeFilters.length > 0 || filters.keyword

  const content = (
    <main className={`page-content ${!isAuthenticated ? 'no-sidebar' : ''}`}>
      <div className="page-title">Explore Schemes</div>
      <div className="page-subtitle">Browse {total.toLocaleString()} government schemes</div>

      <div className="explorer-filters card">
        {/* Search */}
        <div className="search-bar">
          <span className="search-icon">🔍</span>
          <input
            className="search-input"
            placeholder="Search by name, keyword, benefit..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
          />
          {searchInput && (
            <button className="search-clear" onClick={() => setSearchInput('')}>✕</button>
          )}
        </div>

        {/* Filter Row */}
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

          <select className="form-select filter-select" value={filters.state} onChange={(e) => setFilter('state', e.target.value)}>
            <option value="">All States</option>
            {INDIAN_STATES.map((s) => <option key={s} value={s}>{s}</option>)}
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
            <button className="btn btn-ghost btn-sm" onClick={clearAll}>✕ Clear All</button>
          )}
        </div>

        {/* Tag chips */}
        {tags.length > 0 && (
          <div className="tag-chips">
            {tags.map((t) => (
              <button
                key={t}
                className={`tag-chip ${filters.tag === t ? 'active' : ''}`}
                onClick={() => setFilter('tag', filters.tag === t ? '' : t)}
              >
                {t}
              </button>
            ))}
          </div>
        )}

        {/* Active filter badges */}
        {activeFilters.length > 0 && (
          <div className="active-filters">
            {activeFilters.map(({ key, label }) => (
              <span key={key} className="filter-badge">
                {label}
                <button onClick={() => setFilter(key, '')}>✕</button>
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Results */}
      {loading ? (
        <div className="loading-center"><div className="loading-spinner" /></div>
      ) : schemes.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🔍</div>
          <h3>No schemes found</h3>
          <p>Try different keywords or clear the filters.</p>
          {hasFilters && <button className="btn btn-primary btn-sm" onClick={clearAll}>Clear Filters</button>}
        </div>
      ) : (
        <>
          <div className="explorer-results-info">
            Showing {((filters.page - 1) * 12) + 1}–{Math.min(filters.page * 12, total)} of {total.toLocaleString()} schemes
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
