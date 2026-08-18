import { apiRequest } from "./api";
import type { FocusSession } from "./types";

async function readResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`Focus Service request failed (${response.status}).`);
  }
  return response.json() as Promise<T>;
}

export async function listSessions(): Promise<FocusSession[]> {
  return readResponse<FocusSession[]>(await apiRequest("/sessions"));
}

export async function createSession(
  topic: string,
  plannedDuration: number,
): Promise<FocusSession> {
  return readResponse<FocusSession>(
    await apiRequest("/sessions", {
      method: "POST",
      body: JSON.stringify({
        topic,
        planned_duration: plannedDuration,
      }),
    }),
  );
}

export async function startSession(id: string): Promise<FocusSession> {
  return action(id, "start");
}

export async function completeSession(id: string): Promise<FocusSession> {
  return action(id, "complete");
}

export async function cancelSession(id: string): Promise<FocusSession> {
  return action(id, "cancel");
}

async function action(id: string, name: "start" | "complete" | "cancel") {
  return readResponse<FocusSession>(
    await apiRequest(`/sessions/${id}/${name}`, { method: "POST" }),
  );
}
