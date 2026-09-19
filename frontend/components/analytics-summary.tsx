"use client";

import type { AnalyticsSummary } from "../lib/types";
import { formatReadableDuration } from "../lib/format";

export function AnalyticsSummaryCard({ summary }: { summary: AnalyticsSummary }) {
  return (
    <section className="card supporting-card">
      <h2>Overview</h2>
      <div className="metric-grid">
        <span><small>Today focus</small><strong>{formatReadableDuration(summary.today_focus_seconds)}</strong></span>
        <span><small>Today sessions</small><strong>{summary.today_completed_sessions}</strong></span>
        <span><small>This week</small><strong>{formatReadableDuration(summary.week_focus_seconds)}</strong></span>
        <span><small>Week sessions</small><strong>{summary.week_completed_sessions}</strong></span>
      </div>
      {summary.week_completed_sessions === 0 && summary.top_topic === null ? (
        <p className="muted analytics-note">Complete your first focus session to see your analytics here.</p>
      ) : (
        <p className="muted analytics-note">Top topic: {summary.top_topic ?? "—"}</p>
      )}
    </section>
  );
}
