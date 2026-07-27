import { useState, useEffect, useRef } from 'react'
import { useLocation } from 'react-router-dom'
import Navbar from '../../components/layout/Navbar'
import Sidebar from '../../components/layout/Sidebar'
import BottomNav from '../../components/layout/BottomNav'
import api from '../../services/api'
import './Assistant.css'

function renderMarkdown(text) {
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code class="inline-code">$1</code>')
    .replace(/^### (.+)$/gm, '<h4 class="md-h4">$1</h4>')
    .replace(/^## (.+)$/gm, '<h3 class="md-h3">$1</h3>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>[\s\S]*?<\/li>)/g, '<ul class="md-list">$1</ul>')
    .replace(/\n\n/g, '<br/><br/>')
    .replace(/\n/g, '<br/>')
}

export default function Assistant() {
  const location = useLocation()
  const schemeSlug = location.state?.schemeSlug || null
  const schemeName = location.state?.schemeName || null
  const [messages, setMessages] = useState([
    { role: 'assistant', text: schemeName
        ? `👋 Hi! I'm your NeuraScheme AI Assistant. I can see you're asking about **${schemeName}**. What would you like to know?`
        : '👋 Hi! I\'m your NeuraScheme AI Assistant. Ask me anything about government schemes — eligibility, benefits, documents, or how to apply.'
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [conversationId, setConversationId] = useState(null)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const send = async () => {
    const text = input.trim()
    if (!text || loading) return
    setInput('')
    setMessages((m) => [...m, { role: 'user', text }])
    setLoading(true)
    try {
      const res = await api.post('/ai/assistant', {
        question: text,
        conversation_id: conversationId || null,
        scheme_slugs: schemeSlug ? [schemeSlug] : [],
      })
      setConversationId(res.data.conversation_id)
      setMessages((m) => [...m, { role: 'assistant', text: res.data.response }])
    } catch {
      setMessages((m) => [...m, { role: 'assistant', text: '⚠️ Sorry, I encountered an error. Please try again.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() }
  }

  const clearChat = () => {
    setMessages([{ role: 'assistant', text: '👋 Hi! I\'m your NeuraScheme AI Assistant. Ask me anything about government schemes.' }])
    setConversationId(null)
  }

  const suggestions = [
    'What schemes are available for farmers?',
    'How do I apply for PM Kisan Yojana?',
    'What documents do I need for a scholarship?',
    'Are there schemes for women entrepreneurs?',
  ]

  return (
    <div>
      <Navbar />
      <div className="page-layout">
        <Sidebar />
        <main className="page-content assistant-page">
          <div className="assistant-header">
            <div>
              <div className="page-title">AI Assistant</div>
              <div className="page-subtitle">Ask anything about government schemes</div>
            </div>
            <button className="btn btn-ghost btn-sm" onClick={clearChat}>🗑️ Clear Chat</button>
          </div>

          <div className="chat-container card">
            <div className="chat-messages">
              {messages.map((m, i) => (
                <div key={i} className={`chat-message ${m.role}`}>
                  {m.role === 'assistant' && <div className="chat-avatar">🧠</div>}
                  {m.role === 'assistant'
                    ? <div className="chat-bubble" dangerouslySetInnerHTML={{ __html: renderMarkdown(m.text) }} />
                    : <div className="chat-bubble">{m.text}</div>
                  }
                  {m.role === 'user' && <div className="chat-avatar user-avatar-chat">👤</div>}
                </div>
              ))}
              {loading && (
                <div className="chat-message assistant">
                  <div className="chat-avatar">🧠</div>
                  <div className="chat-bubble typing">
                    <span /><span /><span />
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>

            {messages.length === 1 && (
              <div className="chat-suggestions">
                <p className="suggestions-label">Try asking:</p>
                <div className="suggestions-grid">
                  {suggestions.map((s) => (
                    <button key={s} className="suggestion-btn" onClick={() => { setInput(s) }}>
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="chat-input-row">
              <textarea
                className="chat-input"
                placeholder="Ask about any government scheme..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKey}
                rows={1}
              />
              <button className="chat-send-btn" onClick={send} disabled={!input.trim() || loading}>
                {loading ? '⏳' : '➤'}
              </button>
            </div>
          </div>
        </main>
      </div>
      <BottomNav />
    </div>
  )
}
