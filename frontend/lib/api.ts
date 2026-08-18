"use client";

import { getAccessToken } from "./auth";

function requiredBaseUrl(value: string | undefined, name: string): string {
  if (!value) {
    throw new Error(`${name} is required.`);
  }
  return value.replace(/\/$/, "");
}

async function authenticatedRequest(
  baseUrl: string,
  path: string,
  init: RequestInit = {},
): Promise<Response> {
  const token = await getAccessToken();
  const headers = new Headers(init.headers);
  headers.set("Authorization", `Bearer ${token}`);
  headers.set("Content-Type", "application/json");

  return fetch(`${baseUrl}${path}`, {
    ...init,
    headers,
  });
}

export function apiRequest(
  path: string,
  init: RequestInit = {},
): Promise<Response> {
  const baseUrl = requiredBaseUrl(
    process.env.NEXT_PUBLIC_API_BASE_URL,
    "NEXT_PUBLIC_API_BASE_URL",
  );
  return authenticatedRequest(baseUrl, path, init);
}

export function analyticsRequest(
  path: string,
  init: RequestInit = {},
): Promise<Response> {
  const baseUrl = requiredBaseUrl(
    process.env.NEXT_PUBLIC_ANALYTICS_API_BASE_URL,
    "NEXT_PUBLIC_ANALYTICS_API_BASE_URL",
  );
  return authenticatedRequest(baseUrl, path, init);
}
