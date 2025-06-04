import { useEffect, useState } from 'react'
import CitationsDrawer from './CitationsDrawer'

const sessionId = 'default'

export default function ChatWindow() {
  const [messages, setMessages] = useState<string[]>(
    JSON.parse(localStorage.getItem('chat_history') || '[]')
  )
  const [citations, setCitations] = useState<string[]>([])
  const [input, setInput] = useState('')
  const [search, setSearch] = useState('')
  const [results, setResults] = useState<{ document_id: number; text: string }[]>([])
  const [file, setFile] = useState<File | null>(null)
  const [profileOpen, setProfileOpen] = useState(false)
  const [ws, setWs] = useState<WebSocket | null>(null)

  useEffect(() => {
    const socket = new WebSocket(`ws://localhost:8000/ws/chat/${sessionId}/`)
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'ai.message') {
        setMessages((prev) => {
          const updated = [...prev, data.content]
          localStorage.setItem('chat_history', JSON.stringify(updated))
          return updated
        })
        if (data.citations) setCitations(data.citations)
      }
    }
    setWs(socket)
    return () => socket.close()
  }, [])

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault()
    if (!ws || !input) return
    ws.send(JSON.stringify({ type: 'user.message', content: input }))
    setMessages((prev) => {
      const updated = [...prev, input]
      localStorage.setItem('chat_history', JSON.stringify(updated))
      return updated
    })
    setInput('')
  }

  const handleSearch = async (q: string) => {
    setSearch(q)
    if (!q) {
      setResults([])
      return
    }
    const res = await fetch(`/v1/search/?q=${encodeURIComponent(q)}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    })
    if (res.ok) {
      const data = await res.json()
      setResults(data.results)
    }
  }

  const uploadDocument = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    await fetch('/v1/upload/', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: formData,
    })
    setFile(null)
  }

  return (
    <div className="d-flex" style={{ height: '100vh' }}>
      <div className="border-end p-3" style={{ width: '250px', overflowY: 'auto' }}>
        <h5>History</h5>
        {messages.map((m, i) => (
          <div key={i} className="mb-2">
            {m}
          </div>
        ))}
      </div>
      <div className="flex-grow-1 d-flex flex-column">
        <div className="d-flex justify-content-between align-items-center border-bottom p-2">
          <input
            className="form-control me-2"
            placeholder="Search..."
            value={search}
            onChange={(e) => handleSearch(e.target.value)}
            style={{ maxWidth: '300px' }}
          />
          <div className="position-relative">
            <button className="btn btn-secondary" onClick={() => setProfileOpen(!profileOpen)}>
              <i className="bi bi-person-circle"></i>
            </button>
            {profileOpen && (
              <div className="position-absolute end-0 mt-2 p-2 border bg-white shadow" style={{ minWidth: '200px' }}>
                <div className="mb-2">User: admin</div>
                <div>Token: {localStorage.getItem('access_token')?.slice(0, 10)}...</div>
              </div>
            )}
          </div>
        </div>
        <div className="p-3 flex-grow-1 overflow-auto">
          {messages.map((m, i) => (
            <div key={i} className="mb-2">
              {m}
            </div>
          ))}
          <CitationsDrawer citations={citations} />
          {results.length > 0 && (
            <div className="mt-3">
              <h5>Search Results</h5>
              <ul>
                {results.map((r) => (
                  <li key={r.document_id}>{r.text}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
        <form onSubmit={sendMessage} className="p-3 border-top d-flex">
          <input
            className="form-control me-2"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message"
          />
          <button className="btn btn-primary" type="submit">
            Send
          </button>
        </form>
        <form onSubmit={uploadDocument} className="p-3 border-top d-flex">
          <input type="file" className="form-control me-2" onChange={(e) => setFile(e.target.files?.[0] || null)} />
          <button className="btn btn-secondary" type="submit">
            Upload
          </button>
        </form>
      </div>
    </div>
  )
}
