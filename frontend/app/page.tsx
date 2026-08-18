"use client";

import { useEffect, useMemo, useState } from "react";

import { AnalyticsSummaryCard } from "../components/analytics-summary";
import { FocusTimer } from "../components/focus-timer";
import { SessionForm } from "../components/session-form";
import { SessionHistory } from "../components/session-history";
import { useFocusSessions } from "../hooks/use-focus-sessions";
import { getAnalyticsSummary } from "../lib/analytics-api";
import {
  getAuthenticatedUser,
  login,
  logout,
} from "../lib/auth";
import type { AnalyticsSummary } from "../lib/types";

export default function Home() {
  const [authenticated, setAuthenticated] = useState(false);
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { sessions, loading, loadSessions, addSession, transition } = useFocusSessions();

  const activeSession = useMemo(
    () => sessions.find((session) => session.status === "running") ?? sessions.find((session) => session.status === "pending"),
    [sessions],
  );

  useEffect(() => {
    getAuthenticatedUser()
      .then((user) => setAuthenticated(Boolean(user && !user.expired)))
      .catch(() => setAuthenticated(false));
  }, []);

  useEffect(() => {
    if (!authenticated) return;
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    Promise.all([loadSessions(), getAnalyticsSummary(timezone)])
      .then(([, summary]) => setAnalytics(summary))
      .catch((reason: unknown) => setError(reason instanceof Error ? reason.message : "Could not load dashboard."));
  }, [authenticated, loadSessions]);

  async function create(topic: string, duration: number) {
    setError(null);
    try {
      await addSession(topic, duration);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Could not create session.");
    }
  }

  async function action(name: "start" | "complete" | "cancel") {
    if (!activeSession) return;
    setError(null);
    try {
      await transition(activeSession.id, name);
      if (name === "complete") {
        const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        setAnalytics(await getAnalyticsSummary(timezone));
      }
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Could not update session.");
    }
  }

  return (
    <main className="page-shell">
      <h1>Time&amp;You</h1>
      <p>Focus sessions, kept simple.</p>
      {authenticated ? (
        <button type="button" onClick={() => void logout()}>
          Sign out
        </button>
      ) : (
        <button type="button" onClick={() => void login()}>
          Sign in
        </button>
      )}
      {authenticated && (
        <div className="dashboard">
          {error && <p className="error" role="alert">{error}</p>}
          {analytics && <AnalyticsSummaryCard summary={analytics} />}
          <SessionForm onCreate={create} />
          {activeSession && <FocusTimer session={activeSession} onAction={action} />}
          {loading ? <p className="muted">Loading sessions…</p> : <SessionHistory sessions={sessions} />}
        </div>
      )}
    </main>
  );
}
