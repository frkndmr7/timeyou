"use client";

import { useEffect, useState } from "react";

import type { FocusSession } from "../lib/types";

type FocusTimerProps = {
  session: FocusSession;
  onAction: (action: "start" | "complete" | "cancel") => Promise<void>;
};

function elapsedSeconds(startedAt: string | null, now: number) {
  if (!startedAt) return 0;
  return Math.max(0, Math.floor((now - Date.parse(startedAt)) / 1000));
}

function formatDuration(seconds: number) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, "0");
  const remaining = (seconds % 60).toString().padStart(2, "0");
  return `${minutes}:${remaining}`;
}

export function FocusTimer({ session, onAction }: FocusTimerProps) {
  const [now, setNow] = useState(() => Date.now());
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (session.status !== "running") return;
    const timer = window.setInterval(() => setNow(Date.now()), 1000);
    return () => window.clearInterval(timer);
  }, [session.status]);

  async function action(name: "start" | "complete" | "cancel") {
    setBusy(true);
    try {
      await onAction(name);
    } finally {
      setBusy(false);
    }
  }

  const elapsed = elapsedSeconds(session.started_at, now);
  return (
    <section className="card primary-card timer-card">
      <div>
        <p className="eyebrow">Current session</p>
        <h2>{session.topic}</h2>
        <p className="muted">{session.status}</p>
      </div>
      <strong className="timer">{formatDuration(elapsed)}</strong>
      <p className="muted">Planned: {formatDuration(session.planned_duration)}</p>
      <div className="button-row">
        {session.status === "pending" && <button disabled={busy} onClick={() => void action("start")}>Start</button>}
        {session.status === "running" && <button disabled={busy} onClick={() => void action("complete")}>Complete</button>}
        {(session.status === "pending" || session.status === "running") && <button className="secondary" disabled={busy} onClick={() => void action("cancel")}>Cancel</button>}
      </div>
    </section>
  );
}
