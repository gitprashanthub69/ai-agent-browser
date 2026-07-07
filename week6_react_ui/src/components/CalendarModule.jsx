import { useState, useEffect } from "react";

export default function CalendarModule() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [newEvent, setNewEvent] = useState({ summary: "", start_time: "", end_time: "", description: "" });
  const [status, setStatus] = useState(null);

  async function fetchEvents() {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/calendar/events");
      const data = await res.json();
      if (data.events) setEvents(data.events);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  }

  useEffect(() => {
    fetchEvents();
  }, []);

  async function handleAddEvent() {
    setLoading(true);
    setStatus(null);
    try {
      const res = await fetch("http://localhost:8000/api/calendar/events", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newEvent),
      });
      if (!res.ok) throw new Error("Failed to add event");
      setStatus("✅ Event added successfully!");
      setNewEvent({ summary: "", start_time: "", end_time: "", description: "" });
      fetchEvents();
    } catch (err) {
      setStatus("❌ " + err.message);
    }
    setLoading(false);
  }

  return (
    <div className="module-panel">
      <h2>Calendar Integration</h2>
      <p>View upcoming schedule and add events.</p>

      <div className="glass-panel" style={{marginBottom: '20px', padding: '15px'}}>
        <h3>Upcoming Events</h3>
        {loading && <p>Loading...</p>}
        {!loading && events.length === 0 && <p>No upcoming events.</p>}
        <ul>
          {events.map((ev, i) => (
            <li key={i}>
              <strong>{ev.summary}</strong> — {new Date(ev.start.dateTime || ev.start.date).toLocaleString()}
            </li>
          ))}
        </ul>
      </div>

      <div className="form">
        <h3>Add New Event</h3>
        <div className="field">
          <label>Event Title</label>
          <input 
            type="text" 
            value={newEvent.summary} 
            onChange={(e) => setNewEvent({...newEvent, summary: e.target.value})} 
          />
        </div>
        <div className="field">
          <label>Start Time (ISO 8601)</label>
          <input 
            type="text" 
            value={newEvent.start_time} 
            placeholder="2026-07-08T10:00:00Z"
            onChange={(e) => setNewEvent({...newEvent, start_time: e.target.value})} 
          />
        </div>
        <div className="field">
          <label>End Time (ISO 8601)</label>
          <input 
            type="text" 
            value={newEvent.end_time} 
            placeholder="2026-07-08T11:00:00Z"
            onChange={(e) => setNewEvent({...newEvent, end_time: e.target.value})} 
          />
        </div>
        <button onClick={handleAddEvent} disabled={loading || !newEvent.summary}>
          {loading ? "Adding..." : "Add Event"}
        </button>
        {status && <p className="save-status">{status}</p>}
      </div>
    </div>
  );
}
