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
          {steps.map((step, i) => (
            <li
              key={`${step}-${i}`}
              className={
                step.startsWith("❌")
                  ? "step error"
                  : step.startsWith("✅")
                  ? "step success"
                  : step === "🏁 DONE"
                  ? "step done"
                  : "step info"
              }
            >
              <span className="step-num">{i + 1}</span>
              <span>{step}</span>
            </li>
          ))}
          <li ref={bottomRef} className="step info" />
        </ul>
      )}
    </div>
  );
}
