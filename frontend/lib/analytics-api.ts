import { analyticsRequest } from "./api";
import type { AnalyticsSummary } from "./types";

export async function getAnalyticsSummary(
  timezone: string,
): Promise<AnalyticsSummary> {
  const response = await analyticsRequest(
    `/analytics/summary?timezone=${encodeURIComponent(timezone)}`,
  );
  if (!response.ok) {
    throw new Error(`Analytics Service request failed (${response.status}).`);
  }
  return response.json() as Promise<AnalyticsSummary>;
}
