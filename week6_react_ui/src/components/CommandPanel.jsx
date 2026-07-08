import { useState } from "react";

const API_BASE = "http://localhost:8000";

export default function CommandPanel({ onTaskStart, onStep, onTaskComplete }) {
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
        if (event.data.includes("🏁 DONE")) {
          ws.close();
          setLoading(false);
          if (onTaskComplete) onTaskComplete();
        } else {
          onStep(event.data);
        }
      };

      ws.onerror = () => {
        setError("WebSocket error — ensure the FastAPI server is running.");
        setLoading(false);
        if (onTaskComplete) onTaskComplete();
      };

      ws.onclose = () => {
        setLoading(false);
        if (onTaskComplete) onTaskComplete();
      };
    } catch (err) {
      setError(err.message || "Unable to start the agent.");
      setLoading(false);
    }
  }

  function handleKey(e) {
    if (e.key === "Enter" && !loading) handleSubmit();
  }

  function handleMouseMove(e) {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    e.currentTarget.style.setProperty("--mouse-x", `${x}px`);
    e.currentTarget.style.setProperty("--mouse-y", `${y}px`);
  }

  return (
    <div className="command-panel" onMouseMove={handleMouseMove}>
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
          <li onClick={() => setCommand("Search YouTube for LangChain tutorial")}>Search YouTube for LangChain tutorial</li>
          <li onClick={() => setCommand("Search GitHub for FastAPI projects")}>Search GitHub for FastAPI projects</li>
          <li onClick={() => setCommand("Search for Python interview questions 2025")}>Search for Python interview questions 2025</li>
          <li onClick={() => setCommand("Search Reddit for AI tools for students")}>Search Reddit for AI tools for students</li>
        </ul>
      </div>
    </div>
  );
}
