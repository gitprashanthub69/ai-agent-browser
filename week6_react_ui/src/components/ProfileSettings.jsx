import { useEffect, useState } from "react";

const API_BASE = "http://localhost:8000";

export default function ProfileSettings() {
  const [profile, setProfile] = useState({
    name: "",
    email: "",
    phone: "",
    address: "",
    resume_text: "",
  });
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/user/profile`)
      .then((r) => (r.ok ? r.json() : null))
      .then((data) => {
        if (data) setProfile(data);
      })
      .catch(() => {});
  }, []);

  async function handleSave() {
    setLoading(true);
    setStatus(null);
    try {
      const res = await fetch(`${API_BASE}/user/profile`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(profile),
      });
      if (!res.ok) throw new Error("Save failed");
      setStatus("✅ Profile saved successfully!");
    } catch (err) {
      setStatus(`❌ ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  function handleChange(e) {
    setProfile((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  }

  function handleMouseMove(e) {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    e.currentTarget.style.setProperty("--mouse-x", `${x}px`);
    e.currentTarget.style.setProperty("--mouse-y", `${y}px`);
  }

  return (
    <div className="profile-settings" onMouseMove={handleMouseMove}>
      <h2>User Profile</h2>
      <p className="hint">The agent uses this profile to prefill forms and assist with tasks.</p>

      <div className="form">
        {[
          { label: "Full Name", name: "name", type: "text" },
          { label: "Email", name: "email", type: "email" },
          { label: "Phone", name: "phone", type: "tel" },
          { label: "Address", name: "address", type: "text" },
        ].map(({ label, name, type }) => (
          <div className="field" key={name}>
            <label>{label}</label>
            <input
              type={type}
              name={name}
              value={profile[name]}
              onChange={handleChange}
              placeholder={label}
            />
          </div>
        ))}

        <div className="field">
          <label>Resume Text</label>
          <textarea
            name="resume_text"
            value={profile.resume_text}
            onChange={handleChange}
            rows={4}
            placeholder="Paste your resume text here"
          />
        </div>

        <button onClick={handleSave} disabled={loading}>
          {loading ? "Saving…" : "Save Profile"}
        </button>

        {status && <p className="save-status">{status}</p>}
      </div>
    </div>
  );
}
