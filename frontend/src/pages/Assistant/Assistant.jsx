import { useState, useEffect, useRef } from 'react'
import { useLocation } from 'react-router-dom'
import Navbar from '../../components/layout/Navbar'
import Sidebar from '../../components/layout/Sidebar'
import BottomNav from '../../components/layout/BottomNav'
import { Brain, Target, Scale, FileText, Clock, MessageSquare, Pencil, Trash2, Send, Loader2, User } from 'lucide-react'
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

function timeAgo(isoString) {
  if (!isoString) return ''
  const diff = Date.now() - new Date(isoString).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return 'Just now'
  if (mins < 60) return `${mins}m ago`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs}h ago`
  return `${Math.floor(hrs / 24)}d ago`
}

const AGENT_LABELS = {
  recommendations: { icon: Target, label: 'Recommendations' },
  comparison: { icon: Scale, label: 'Comparison' },
  documents: { icon: FileText, label: 'Documents' },
  deadlines: { icon: Clock, label: 'Deadlines' },
  general: { icon: MessageSquare, label: 'General' },
}

const WELCOME = "Hi! I'm your NeuraScheme AI Assistant. Ask me anything about government schemes — eligibility, benefits, documents, or how to apply."

export default function Assistant() {
  const location = useLocation()
  const schemeSlug = location.state?.schemeSlug || null
  const schemeName = location.state?.schemeName || null

  const [messages, setMessages] = useState([
    { role: 'assistant', text: schemeName
        ? `Hi! I'm your NeuraScheme AI Assistant. I can see you're asking about **${schemeName}**. What would you like to know?`
        : WELCOME
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [conversationId, setConversationId] = useState(null)
  const [history, setHistory] = useState([])
  const [historyOpen, setHistoryOpen] = useState(true)
  const [historyLoading, setHistoryLoading] = useState(true)
  const [activeConvId, setActiveConvId] = useState(null)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    setHistoryLoading(true)
    try {
      const res = await api.get('/ai/conversations')
      setHistory(res.data || [])
    } catch {
      setHistory([])
    } finally {
      setHistoryLoading(false)
    }
  }

  const openConversation = (conv) => {
    const msgs = [{ role: 'assistant', text: WELCOME }]
    for (const m of conv.messages) {
      msgs.push({ role: 'user', text: m.question })
      msgs.push({ role: 'assistant', text: m.response })
    }
    setMessages(msgs)
    setConversationId(conv.conversation_id)
    setActiveConvId(conv.conversation_id)
  }

  const newChat = () => {
    setMessages([{ role: 'assistant', text: WELCOME }])
    setConversationId(null)
    setActiveConvId(null)
    setInput('')
  }

  const deleteConversation = async (e, convId) => {
    e.stopPropagation()
    try {
      await api.delete(`/ai/conversations/${convId}`)
      setHistory((h) => h.filter((c) => c.conversation_id !== convId))
      if (activeConvId === convId) newChat()
    } catch {}
  }

  const sendText = async (text) => {
    if (!text.trim() || loading) return
    setInput('')
    setMessages((m) => [...m, { role: 'user', text }])
    setLoading(true)
    try {
      const res = await api.post('/ai/assistant', {
        question: text,
        conversation_id: conversationId || null,
        scheme_slugs: schemeSlug ? [schemeSlug] : [],
      })
      const newConvId = res.data.conversation_id
      setConversationId(newConvId)
      setActiveConvId(newConvId)
      const agentsUsed = res.data.agents_used || []
      setMessages((m) => [...m, { role: 'assistant', text: res.data.response, agents: agentsUsed }])
      loadHistory()
    } catch {
      setMessages((m) => [...m, { role: 'assistant', text: 'Sorry, I encountered an error. Please try again.' }])
    } finally {
      setLoading(false)
    }
  }

  const send = () => sendText(input.trim())

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() }
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

          <div className="assistant-layout">
            {/* History Panel */}
            <div className={`history-panel ${historyOpen ? 'open' : 'closed'}`}>
              <div className="history-panel-header">
                {historyOpen && <span className="history-panel-title">Chat History</span>}
                <button
                  className={`panel-toggle-btn ${historyOpen ? 'open' : ''}`}
                  onClick={() => setHistoryOpen((o) => !o)}
                  title={historyOpen ? 'Close history' : 'Open history'}
                >
                  <span /><span /><span />
                </button>
              </div>

              {historyOpen && (
                <>
                  <button className="new-chat-btn" onClick={newChat}>
                    <Pencil size={14} /> New Chat
                  </button>

                  <div className="history-list">
                    {historyLoading ? (
                      <div className="history-empty">Loading...</div>
                    ) : history.length === 0 ? (
                      <div className="history-empty">No past conversations</div>
                    ) : (
                      history.map((conv) => {
                        const firstQ = conv.messages?.[0]?.question || 'Conversation'
                        const lastMsg = conv.messages?.[conv.messages.length - 1]
                        const preview = lastMsg?.question || firstQ
                        return (
                          <div
                            key={conv.conversation_id}
                            className={`history-item ${activeConvId === conv.conversation_id ? 'active' : ''}`}
                            onClick={() => openConversation(conv)}
                          >
                            <div className="history-item-text">
                              <div className="history-item-preview">{preview}</div>
                              <div className="history-item-time">{timeAgo(conv.updatedAt)} · {conv.messages?.length || 0} msgs</div>
                            </div>
                            <button
                              className="history-delete-btn"
                              onClick={(e) => deleteConversation(e, conv.conversation_id)}
                              title="Delete"
                            >
                              <Trash2 size={14} />
                            </button>
                          </div>
                        )
                      })
                    )}
                  </div>
                </>
              )}
            </div>

            {/* Chat Area */}
            <div className="chat-area">
              <div className="assistant-header">
                <div>
                  <div className="page-title">AI Assistant</div>
                  <div className="page-subtitle">Ask anything about government schemes</div>
                </div>
              </div>

              <div className="chat-container card">
                <div className="chat-messages">
                  {messages.map((m, i) => (
                    <div key={i} className={`chat-message ${m.role}`}>
                      {m.role === 'assistant' && (
                        <div className="chat-avatar"><Brain size={16} /></div>
                      )}
                      {m.role === 'assistant'
                        ? <div className="chat-bubble">
                            {m.agents && m.agents.length > 0 && (
                              <div className="agents-used">
                                {m.agents.map(a => {
                                  const ag = AGENT_LABELS[a]
                                  const AgIcon = ag?.icon || MessageSquare
                                  return (
                                    <span key={a} className="agent-tag">
                                      <AgIcon size={11} /> {ag?.label || a}
                                    </span>
                                  )
                                })}
                              </div>
                            )}
                            <div dangerouslySetInnerHTML={{ __html: renderMarkdown(m.text) }} />
                          </div>
                        : <div className="chat-bubble">{m.text}</div>
                      }
                      {m.role === 'user' && (
                        <div className="chat-avatar user-avatar-chat"><User size={16} /></div>
                      )}
                    </div>
                  ))}
                  {loading && (
                    <div className="chat-message assistant">
                      <div className="chat-avatar"><Brain size={16} /></div>
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
                        <button key={s} className="suggestion-btn" onClick={() => sendText(s)}>
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
                    {loading ? <Loader2 size={16} className="spin" /> : <Send size={16} />}
                  </button>
                </div>
              </div>
            </div>
          </div>

        </main>
      </div>
      <BottomNav />
    </div>
  )
}
