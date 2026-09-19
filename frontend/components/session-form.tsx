"use client";

import { FormEvent, useState } from "react";

type SessionFormProps = {
  onCreate: (topic: string, duration: number) => Promise<void>;
};

export function SessionForm({ onCreate }: SessionFormProps) {
  const [topic, setTopic] = useState("");
  const [duration, setDuration] = useState("25");
  const [saving, setSaving] = useState(false);
  const [topicError, setTopicError] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const plannedDurationMinutes = Number(duration);
    if (!topic.trim()) {
      setTopicError(true);
      return;
    }
    if (!Number.isInteger(plannedDurationMinutes) || plannedDurationMinutes <= 0) {
      return;
    }
    setSaving(true);
    try {
      await onCreate(topic.trim(), plannedDurationMinutes * 60);
      setTopic("");
      setTopicError(false);
    } finally {
      setSaving(false);
    }
  }

  return (
    <form className="card form-stack" noValidate onSubmit={submit}>
      <h2>New focus session</h2>
      <label>
        Topic
        <input
          required
          aria-invalid={topicError}
          aria-describedby={topicError ? "topic-error" : undefined}
          value={topic}
          onChange={(event) => {
            setTopic(event.target.value);
            if (event.target.value.trim()) setTopicError(false);
          }}
          placeholder="What will you focus on?"
        />
      </label>
      {topicError && <p className="error" id="topic-error" role="alert">Enter a topic to create a session.</p>}
      <label>
        Planned duration (minutes)
        <input type="number" min="1" step="1" value={duration} onChange={(event) => setDuration(event.target.value)} />
      </label>
      <button type="submit" disabled={saving}>{saving ? "Creating…" : "Create session"}</button>
    </form>
  );
}
