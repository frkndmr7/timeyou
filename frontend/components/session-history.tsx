"use client";

import type { FocusSession } from "../lib/types";
import { formatReadableDuration } from "../lib/format";

export function SessionHistory({ sessions }: { sessions: FocusSession[] }) {
  return (
    <section className="card supporting-card">
      <h2>Session history</h2>
      {sessions.length === 0 ? <p className="muted">No sessions yet.</p> : (
        <ul className="session-list">
          {sessions.map((session) => (
            <li key={session.id}>
              <span>
                <strong className="session-topic">{session.topic}</strong>
                <small>{formatReadableDuration(session.planned_duration)} planned</small>
              </span>
              <span className={`status status-${session.status}`}>{session.status}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
