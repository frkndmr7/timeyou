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

  if (!authenticated) {
    return (
      <main className="page-shell landing-shell">
        <div className="landing-frame">
          <header className="landing-header">
            <div className="landing-brand">
              <span className="landing-mark" aria-hidden="true" />
              <span>Time&amp;You</span>
            </div>
          </header>
          <section className="landing-content" aria-labelledby="landing-title">
            <div className="landing-copy">
              <p className="landing-eyebrow">A little more focus, every day</p>
              <h1 id="landing-title">Make time for what matters.</h1>
              <p className="landing-description">
                Track your focus sessions and understand where your time goes.
              </p>
              <button className="landing-cta" type="button" onClick={() => void login()}>
                Sign in
              </button>
            </div>
            <div className="landing-art" aria-hidden="true">
              <span className="landing-orbit landing-orbit-outer" />
              <span className="landing-orbit landing-orbit-inner" />
              <span className="landing-orbit-dot" />
              <span className="landing-art-label">TIME, WELL SPENT</span>
            </div>
          </section>
        </div>
      </main>
    );
  }

  return (
    <main className="page-shell">
      <header className="app-header">
        <div className="brand">
          <h1>Time&amp;You</h1>
          <p>Focus sessions, kept simple.</p>
        </div>
        {authenticated ? (
          <button className="secondary auth-action" type="button" onClick={() => void logout()}>
            Sign out
          </button>
        ) : (
          <button className="auth-action" type="button" onClick={() => void login()}>
            Sign in
          </button>
        )}
      </header>
      {authenticated && (
        <div className="dashboard">
          {error && <p className="error error-message" role="alert">{error}</p>}
          <div className="dashboard-primary">
            {activeSession && <FocusTimer session={activeSession} onAction={action} />}
            <SessionForm onCreate={create} />
          </div>
          <aside className="dashboard-supporting" aria-label="Session overview">
            {analytics && <AnalyticsSummaryCard summary={analytics} />}
            {loading ? (
              <p className="muted loading-state" role="status">Loading sessions…</p>
            ) : (
              <SessionHistory sessions={sessions} />
            )}
          </aside>
        </div>
      )}
    </main>
  );
}
