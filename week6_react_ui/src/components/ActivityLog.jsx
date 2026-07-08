import { useEffect, useRef } from "react";

export default function ActivityLog({ steps, taskId }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [steps]);

  return (
    <div className="activity-log">
      <h2>
        Activity Log
        {taskId && <span className="task-id">#{taskId.slice(0, 8)}</span>}
      </h2>

      {steps.length === 0 ? (
        <p className="empty">Agent steps will appear here as the task runs…</p>
      ) : (
        <ul className="steps">
          {steps.map((step, i) => {
            const parts = step.split("|||");
            const displayStep = parts[0];
            const url = parts[1] ? parts[1].trim() : null;

            return (
              <li
                key={`${step}-${i}`}
                className={
                  displayStep.startsWith("❌")
                    ? "step error"
                    : displayStep.startsWith("✅")
                    ? "step success"
                    : displayStep === "🏁 DONE"
                    ? "step done"
                    : "step info"
                }
              >
                <span className="step-num">{i + 1}</span>
                <span style={{ display: "flex", width: "100%", justifyContent: "space-between", alignItems: "center" }}>
                  <span>{displayStep}</span>
                  {url && (
                    <a
                      href={url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="step-link"
                    >
                      Visit ↗
                    </a>
                  )}
                </span>
              </li>
            );
          })}
          <li ref={bottomRef} className="step info" />
        </ul>
      )}
    </div>
  );
}
