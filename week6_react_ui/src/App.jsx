import { useState } from "react";
import CommandPanel from "./components/CommandPanel";
import ActivityLog from "./components/ActivityLog";
import ProfileSettings from "./components/ProfileSettings";
import FormModule from "./components/FormModule";
import EmailModule from "./components/EmailModule";
import SummaryModule from "./components/SummaryModule";
import CalendarModule from "./components/CalendarModule";
import MemoryModule from "./components/MemoryModule";
import "./App.css";

export default function App() {
  const [page, setPage] = useState("agent");
  const [taskId, setTaskId] = useState(null);
  const [steps, setSteps] = useState([]);
  const [isRunning, setIsRunning] = useState(false);

  const TABS = [
    { id: "agent", icon: "🤖", label: "Agent" },
    { id: "form", icon: "📋", label: "Form Filler" },
    { id: "email", icon: "📧", label: "Email" },
    { id: "summary", icon: "📄", label: "Summariser" },
    { id: "calendar", icon: "📅", label: "Calendar" },
    { id: "memory", icon: "🧠", label: "Memory" },
    { id: "profile", icon: "⚙️", label: "Profile" },
  ];

  return (
    <div className="app-shell" style={{display: 'flex', flexDirection: 'row', height: '100vh', overflow: 'hidden'}}>
      <div className="ambient ambient-a" />
      <div className="ambient ambient-b" />
      <div className="ambient ambient-c" />

      <div className="particles">
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
      </div>

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

      {/* SIDEBAR */}
      <nav className="sidebar" style={{width: '260px', padding: '30px 20px', borderRight: '1px solid rgba(255,255,255,0.05)', display: 'flex', flexDirection: 'column', zIndex: 10, background: 'rgba(5, 5, 10, 0.6)', backdropFilter: 'blur(20px)'}}>
        <div className="brand-block" style={{marginBottom: '40px', display: 'flex', alignItems: 'center', gap: '12px'}}>
          <div className="brand-mark">✦</div>
          <div>
            <p className="brand-title" style={{fontSize: '1.2rem', margin: 0}}>AI Agent</p>
          </div>
        </div>

        <div className="nav-links" style={{display: 'flex', flexDirection: 'column', gap: '8px'}}>
          {TABS.map(tab => (
            <button
              key={tab.id}
              className={page === tab.id ? "active" : ""}
              onClick={() => setPage(tab.id)}
              style={{
                textAlign: 'left', 
                padding: '12px 16px', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'flex-start',
                width: '100%',
                background: page === tab.id ? 'rgba(255,255,255,0.1)' : 'transparent',
                border: 'none',
                borderRadius: '8px',
                color: page === tab.id ? '#fff' : 'rgba(255,255,255,0.6)',
                fontWeight: page === tab.id ? '600' : '400',
                transition: 'all 0.2s ease'
              }}
            >
              <span style={{marginRight: '12px', fontSize: '1.1rem'}}>{tab.icon}</span> 
              {tab.label}
            </button>
          ))}
        </div>
      </nav>

      {/* MAIN CONTENT AREA */}
      <main className="main-panel" style={{flex: 1, padding: '40px 60px', overflowY: 'auto', zIndex: 10, margin: 0, maxWidth: '100%', display: 'block', height: '100%'}}>
        {page === "agent" && (
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
        )}
        
        {page === "form" && <FormModule />}
        {page === "email" && <EmailModule />}
        {page === "summary" && <SummaryModule />}
        {page === "calendar" && <CalendarModule />}
        {page === "memory" && <MemoryModule />}
        {page === "profile" && <ProfileSettings />}
      </main>
    </div>
  );
}
