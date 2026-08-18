"use client";

import { useCallback, useState } from "react";

import {
  cancelSession,
  completeSession,
  createSession,
  listSessions,
  startSession,
} from "../lib/focus-api";
import type { FocusSession } from "../lib/types";

export function useFocusSessions() {
  const [sessions, setSessions] = useState<FocusSession[]>([]);
  const [loading, setLoading] = useState(false);

  const loadSessions = useCallback(async () => {
    setLoading(true);
    try {
      setSessions(await listSessions());
    } finally {
      setLoading(false);
    }
  }, []);

  const addSession = useCallback(async (topic: string, duration: number) => {
    const session = await createSession(topic, duration);
    setSessions((current) => [session, ...current]);
    return session;
  }, []);

  const transition = useCallback(
    async (id: string, action: "start" | "complete" | "cancel") => {
      const handlers = { start: startSession, complete: completeSession, cancel: cancelSession };
      const session = await handlers[action](id);
      setSessions((current) =>
        current.map((item) => (item.id === session.id ? session : item)),
      );
      return session;
    },
    [],
  );

  return { sessions, loading, loadSessions, addSession, transition };
}
