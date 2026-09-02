"use client";

import { getAccessToken } from "./auth";
import { getRuntimeConfig } from "./runtime-config";

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
  const baseUrl = getRuntimeConfig().apiBaseUrl.replace(/\/$/, "");
  return authenticatedRequest(baseUrl, path, init);
}

export function analyticsRequest(
  path: string,
  init: RequestInit = {},
): Promise<Response> {
  const baseUrl = getRuntimeConfig().analyticsApiBaseUrl.replace(/\/$/, "");
  return authenticatedRequest(baseUrl, path, init);
}
