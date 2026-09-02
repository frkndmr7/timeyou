"use client";

import {
  User,
  UserManager,
  WebStorageStateStore,
} from "oidc-client-ts";
import { getRuntimeConfig } from "./runtime-config";

let userManager: UserManager | undefined;

function getUserManager(): UserManager {
  if (typeof window === "undefined") {
    throw new Error("Cognito authentication is only available in the browser.");
  }

  if (!userManager) {
    const config = getRuntimeConfig();
    userManager = new UserManager({
      authority: config.cognitoIssuer,
      client_id: config.cognitoClientId,
      redirect_uri: config.cognitoRedirectUri,
      post_logout_redirect_uri: config.cognitoLogoutUri,
      response_type: "code",
      scope: "openid",
      stateStore: new WebStorageStateStore({
        store: window.sessionStorage,
      }),
      userStore: new WebStorageStateStore({
        store: window.sessionStorage,
      }),
    });
  }

  return userManager;
}

export function login(): Promise<void> {
  return getUserManager().signinRedirect();
}

export function completeLogin(): Promise<User | undefined> {
  return getUserManager().signinCallback();
}

export function logout(): Promise<void> {
  return getUserManager().signoutRedirect();
}

export function getAuthenticatedUser(): Promise<User | null> {
  return getUserManager().getUser();
}

export async function getAccessToken(): Promise<string> {
  const user = await getAuthenticatedUser();
  if (!user || user.expired) {
    throw new Error("User is not authenticated.");
  }
  return user.access_token;
}
