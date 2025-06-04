export default function CitationsDrawer({ citations }: { citations: string[] }) {
  return (
    <div style={{ border: '1px solid #ccc', padding: '1rem', marginTop: '1rem' }}>
      <h3>Citations</h3>
      <ul>
        {citations.map((c, i) => (
          <li key={i}>{c}</li>
        ))}
      </ul>
    </div>
  )
}
