import { useState } from "react";
import CommandPanel from "./components/CommandPanel";
import ActivityLog from "./components/ActivityLog";
import ProfileSettings from "./components/ProfileSettings";
import "./App.css";

export default function App() {
  const [page, setPage] = useState("agent");
  const [taskId, setTaskId] = useState(null);
  const [steps, setSteps] = useState([]);

  return (
    <div className="app-shell">
      <div className="ambient ambient-a" />
      <div className="ambient ambient-b" />

      <nav className="navbar">
        <div className="brand-block">
          <div className="brand-mark">✦</div>
          <div>
            <p className="brand-title">AI Browser Agent</p>
            <p className="brand-subtitle">Week 6 • React UI</p>
          </div>
        </div>

        <div className="nav-links">
          <button
            className={page === "agent" ? "active" : ""}
            onClick={() => setPage("agent")}
          >
            Agent
          </button>
          <button
            className={page === "profile" ? "active" : ""}
            onClick={() => setPage("profile")}
          >
            Profile
          </button>
        </div>
      </nav>

      <main className="main-panel">
        {page === "agent" ? (
          <div className="agent-layout">
            <CommandPanel
              onTaskStart={(id) => {
                setTaskId(id);
                setSteps([]);
              }}
              onStep={(msg) => setSteps((prev) => [...prev, msg])}
            />
            <ActivityLog steps={steps} taskId={taskId} />
          </div>
        ) : (
          <ProfileSettings />
        )}
      </main>
    </div>
  );
}
