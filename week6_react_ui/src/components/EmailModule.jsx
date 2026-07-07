import { useState } from "react";

export default function EmailModule() {
  const [inbox, setInbox] = useState([]);
  const [draft, setDraft] = useState({ to: "", subject: "", context: "" });
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);

  async function handleSend() {
    setLoading(true);
    setStatus(null);
    try {
      const res = await fetch("http://localhost:8000/api/email/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(draft),
      });
      if (!res.ok) throw new Error("Failed to send");
      setStatus("✅ Email sent successfully!");
      setDraft({ to: "", subject: "", context: "" });
    } catch (err) {
      setStatus("❌ " + err.message);
    }
    setLoading(false);
  }

  async function fetchInbox() {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/email/inbox");
      const data = await res.json();
      if (data.emails) setInbox(data.emails);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  }

  return (
    <div className="module-panel">
      <h2>Email Assistant</h2>
      <p>Draft and send emails, or check recent inbox.</p>
      
      <div className="form">
        <div className="field">
          <label>To:</label>
          <input 
            type="email" 
            value={draft.to} 
            onChange={(e) => setDraft({...draft, to: e.target.value})} 
          />
        </div>
        <div className="field">
          <label>Subject:</label>
          <input 
            type="text" 
            value={draft.subject} 
            onChange={(e) => setDraft({...draft, subject: e.target.value})} 
          />
        </div>
        <div className="field">
          <label>Context / Draft Body:</label>
          <textarea 
            rows={4}
            value={draft.context} 
            onChange={(e) => setDraft({...draft, context: e.target.value})} 
          />
        </div>
        <button onClick={handleSend} disabled={loading || !draft.to}>
          {loading ? "Processing..." : "Send Email"}
        </button>
        {status && <p className="save-status">{status}</p>}
      </div>

      <div style={{marginTop: '40px'}}>
        <button onClick={fetchInbox} className="secondary">Check Inbox</button>
        {inbox.length > 0 && (
          <ul style={{marginTop: '20px'}}>
            {inbox.map((email, idx) => (
              <li key={idx} style={{marginBottom: '10px'}}>
                <strong>{email.subject}</strong> from <em>{email.sender}</em>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
