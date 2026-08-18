"use client";

import { FormEvent, useState } from "react";

type SessionFormProps = {
  onCreate: (topic: string, duration: number) => Promise<void>;
};

export function SessionForm({ onCreate }: SessionFormProps) {
  const [topic, setTopic] = useState("");
  const [duration, setDuration] = useState("25");
  const [saving, setSaving] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const plannedDurationMinutes = Number(duration);
    if (!topic.trim() || !Number.isInteger(plannedDurationMinutes) || plannedDurationMinutes <= 0) {
      return;
    }
    setSaving(true);
    try {
      await onCreate(topic.trim(), plannedDurationMinutes * 60);
      setTopic("");
    } finally {
      setSaving(false);
    }
  }

  return (
    <form className="card form-stack" onSubmit={submit}>
      <h2>New focus session</h2>
      <label>
        Topic
        <input value={topic} onChange={(event) => setTopic(event.target.value)} placeholder="What will you focus on?" />
      </label>
      <label>
        Planned duration (minutes)
        <input type="number" min="1" step="1" value={duration} onChange={(event) => setDuration(event.target.value)} />
      </label>
      <button type="submit" disabled={saving}>{saving ? "Creating…" : "Create session"}</button>
    </form>
  );
}
