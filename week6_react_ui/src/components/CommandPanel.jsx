import { useState } from "react";

const API_BASE = "http://localhost:8000";

export default function CommandPanel({ onTaskStart, onStep }) {
  const [command, setCommand] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit() {
    if (!command.trim()) return;
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API_BASE}/command`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const { task_id } = await res.json();
      onTaskStart(task_id);

      const ws = new WebSocket(`ws://localhost:8000/ws/${task_id}`);

      ws.onmessage = (event) => {
        onStep(event.data);
        if (event.data === "🏁 DONE") {
          ws.close();
          setLoading(false);
        }
      };

      ws.onerror = () => {
        setError("WebSocket error — ensure the FastAPI server is running.");
        setLoading(false);
      };

      ws.onclose = () => setLoading(false);
    } catch (err) {
      setError(err.message || "Unable to start the agent.");
      setLoading(false);
    }
  }

  function handleKey(e) {
    if (e.key === "Enter" && !loading) handleSubmit();
  }

  return (
    <div className="command-panel">
      <h2>Command Center</h2>
      <p className="hint">Describe the browser task you want the agent to perform.</p>

      <div className="input-row">
        <input
          type="text"
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          onKeyDown={handleKey}
          placeholder='Example: "Open Google and search for AI tools"'
          disabled={loading}
        />
        <button onClick={handleSubmit} disabled={loading || !command.trim()}>
          {loading ? "Running…" : "Run"}
        </button>
      </div>

      {error && <p className="error">⚠️ {error}</p>}

      <div className="examples">
        <p>Try these:</p>
        <ul>
          <li onClick={() => setCommand("Go to google.com and search for Python tutorials")}>Go to google.com and search for Python tutorials</li>
          <li onClick={() => setCommand("Fill the contact form with my profile details")}>Fill the contact form with my profile details</li>
          <li onClick={() => setCommand("Summarize the current page")}>Summarize the current page</li>
        </ul>
      </div>
    </div>
  );
}
