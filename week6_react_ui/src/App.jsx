import { useState } from "react";
import CommandPanel from "./components/CommandPanel";
import ActivityLog from "./components/ActivityLog";
import ProfileSettings from "./components/ProfileSettings";
import "./App.css";

export default function App() {
  const [page, setPage] = useState("agent");
  const [taskId, setTaskId] = useState(null);
  const [steps, setSteps] = useState([]);
  const [isRunning, setIsRunning] = useState(false);

  return (
    <div className="app-shell">
      <div className="ambient ambient-a" />
      <div className="ambient ambient-b" />
      <div className="ambient ambient-c" />

      <div className="particles">
        <div className="particle" />
        <div className="particle" />
        <div className="particle" />
        <div className="particle" />
        <div className="particle" />
        <div className="particle" />
        <div className="particle" />
        <div className="particle" />
        <div className="particle" />
        <div className="particle" />
        <div className="particle" />
        <div className="particle" />
      </div>

      {/* 3D Immersive Background Scenes */}
      <div className="scene-3d scene-left">
        <div className="cube-3d outer-cube">
          <div className="cube-face face-front" />
          <div className="cube-face face-back" />
          <div className="cube-face face-right" />
          <div className="cube-face face-left" />
          <div className="cube-face face-top" />
          <div className="cube-face face-bottom" />
        </div>
        <div className="cube-3d inner-cube">
          <div className="cube-face face-front" />
          <div className="cube-face face-back" />
          <div className="cube-face face-right" />
          <div className="cube-face face-left" />
          <div className="cube-face face-top" />
          <div className="cube-face face-bottom" />
        </div>
      </div>

      <div className="scene-3d scene-right">
        <div className="cube-3d outer-cube">
          <div className="cube-face face-front" />
          <div className="cube-face face-back" />
          <div className="cube-face face-right" />
          <div className="cube-face face-left" />
          <div className="cube-face face-top" />
          <div className="cube-face face-bottom" />
        </div>
        <div className="cube-3d inner-cube">
          <div className="cube-face face-front" />
          <div className="cube-face face-back" />
          <div className="cube-face face-right" />
          <div className="cube-face face-left" />
          <div className="cube-face face-top" />
          <div className="cube-face face-bottom" />
        </div>
      </div>


      {/* 3D Holographic Search Globe (Fades in when searching) */}
      <div className={`search-globe-scene ${isRunning ? "active" : ""}`}>
        <div className="globe-3d">
          <div className="globe-ring ring-lat-1" />
          <div className="globe-ring ring-lat-2" />
          <div className="globe-ring ring-lat-3" />
          <div className="globe-ring ring-lon-1" />
          <div className="globe-ring ring-lon-2" />
          <div className="globe-ring ring-lon-3" />
          <div className="globe-core" />
        </div>
      </div>

      <nav className="navbar">
        <div className="brand-block">
          <div className="brand-mark">✦</div>
          <div>
            <p className="brand-title">AI Browser Agent</p>
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
                setIsRunning(true);
              }}
              onTaskComplete={() => setIsRunning(false)}
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
