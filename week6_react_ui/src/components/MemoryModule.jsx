import { useEffect, useState } from "react";

const API_BASE = "http://localhost:8000";

export default function MemoryModule() {
  const [memoryData, setMemoryData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/memory/context`)
      .then((r) => {
        if (!r.ok) throw new Error("Failed to connect to backend");
        return r.json();
      })
      .then((data) => {
        setMemoryData(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="module-panel">
      <h2>Memory Storage</h2>
      <p className="hint">View facts, preferences, and data saved from previous interactions.</p>
      
      {loading && <p style={{marginTop: '20px', opacity: 0.7}}>Connecting to Module 6 Backend...</p>}
      
      {error && (
        <div className="glass-panel" style={{padding: '20px', marginTop: '20px', background: 'rgba(255, 50, 50, 0.1)'}}>
          <p style={{color: '#ff8888'}}>⚠️ {error}</p>
        </div>
      )}

      {memoryData && !loading && (
        <div style={{display: 'flex', flexDirection: 'column', gap: '20px', marginTop: '20px'}}>
          
          <div className="glass-panel" style={{padding: '20px'}}>
            <h3 style={{marginBottom: '15px'}}>Saved User Profile</h3>
            {Object.keys(memoryData.profile || {}).length > 0 ? (
              <pre style={{background: 'rgba(0,0,0,0.2)', padding: '15px', borderRadius: '8px', fontSize: '13px', overflowX: 'auto'}}>
                {JSON.stringify(memoryData.profile, null, 2)}
              </pre>
            ) : (
              <p style={{opacity: 0.7}}>No profile saved in memory yet.</p>
            )}
          </div>

          <div className="glass-panel" style={{padding: '20px'}}>
            <h3 style={{marginBottom: '15px'}}>Form History</h3>
            {memoryData.forms && memoryData.forms.length > 0 ? (
              <ul style={{listStyle: 'none', padding: 0}}>
                {memoryData.forms.map((form, idx) => (
                  <li key={idx} style={{background: 'rgba(255,255,255,0.05)', padding: '12px', borderRadius: '6px', marginBottom: '8px'}}>
                    <strong>{form.form_title || "Unnamed Form"}</strong> - {form.url}
                  </li>
                ))}
              </ul>
            ) : (
              <p style={{opacity: 0.7}}>No form history saved yet.</p>
            )}
          </div>

          <div className="glass-panel" style={{padding: '20px'}}>
            <h3 style={{marginBottom: '15px'}}>Agent Notes</h3>
            {memoryData.notes && memoryData.notes.length > 0 ? (
              <ul style={{listStyle: 'none', padding: 0}}>
                {memoryData.notes.map((note, idx) => (
                  <li key={idx} style={{background: 'rgba(255,255,255,0.05)', padding: '12px', borderRadius: '6px', marginBottom: '8px'}}>
                    <strong>{note.title || "Note"}</strong>
                    <p style={{marginTop: '8px', fontSize: '0.9rem', opacity: 0.8}}>{note.content}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p style={{opacity: 0.7}}>No agent notes saved yet.</p>
            )}
          </div>

        </div>
      )}
    </div>
  );
}
