import { useState } from "react";

export default function FormModule() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);

  async function handleAutoFill() {
    setLoading(true);
    setStatus(null);
    try {
      const res = await fetch("http://localhost:8000/api/fill-form", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      if (!res.ok) throw new Error("Failed to auto-fill form");
      setStatus("✅ Form auto-filled successfully!");
    } catch (err) {
      setStatus("❌ " + err.message);
    }
    setLoading(false);
  }

  return (
    <div className="module-panel">
      <h2>Form Filler</h2>
      <p>Enter a URL containing a form. The AI agent will navigate to it and automatically fill it using your saved profile data.</p>
      <div className="form">
        <div className="field">
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://demoqa.com/automation-practice-form"
          />
        </div>
        <button onClick={handleAutoFill} disabled={loading || !url}>
          {loading ? "Filling..." : "Auto-Fill Form"}
        </button>
        {status && <p className="save-status" style={{marginTop: '15px'}}>{status}</p>}
      </div>
    </div>
  );
}
