export type SessionStatus = "pending" | "running" | "completed" | "cancelled";

export type FocusSession = {
  id: string;
  topic: string;
  planned_duration: number;
  started_at: string | null;
  completed_at: string | null;
  status: SessionStatus;
  created_at: string;
};

export type AnalyticsSummary = {
  today_focus_seconds: number;
  today_completed_sessions: number;
  week_focus_seconds: number;
  week_completed_sessions: number;
  top_topic: string | null;
};
