import { useEffect, useState } from 'react'
import CitationsDrawer from './CitationsDrawer'

const sessionId = 'default'

export default function ChatWindow() {
  const [messages, setMessages] = useState<string[]>([])
  const [citations, setCitations] = useState<string[]>([])

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/chat/${sessionId}/`)
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'ai.message') {
        setMessages((prev) => [...prev, data.content])
        if (data.citations) setCitations(data.citations)
      }
    }
    return () => ws.close()
  }, [])

  return (
    <div>
      <h2>Chat</h2>
      {messages.map((m, i) => (
        <div key={i}>{m}</div>
      ))}
      <CitationsDrawer citations={citations} />
    </div>
  )
}
