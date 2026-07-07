import { useState } from "react";

export default function SummaryModule() {
  const [url, setUrl] = useState("");
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSummarise() {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/summary/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      const data = await res.json();
      setSummary(data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  }

  return (
    <div className="module-panel">
      <h2>Web Summariser</h2>
      <p>Enter a URL to summarize its content using the AI Agent.</p>
      <div className="form">
        <div className="field">
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://en.wikipedia.org/wiki/Python"
          />
        </div>
        <button onClick={handleSummarise} disabled={loading || !url}>
          {loading ? "Summarising..." : "Summarise Page"}
        </button>
      </div>

      {summary && (
        <div className="summary-result glass-panel" style={{marginTop: '20px', padding: '15px'}}>
          <h3>Result</h3>
          <p>{summary.summary}</p>
          <ul>
            {summary.key_points?.map((pt, i) => <li key={i}>{pt}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}
