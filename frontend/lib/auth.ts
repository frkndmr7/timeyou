"use client";

import {
  User,
  UserManager,
  WebStorageStateStore,
} from "oidc-client-ts";

let userManager: UserManager | undefined;

const cognitoEnvironment = {
  issuer: process.env.NEXT_PUBLIC_COGNITO_ISSUER,
  clientId: process.env.NEXT_PUBLIC_COGNITO_CLIENT_ID,
  redirectUri: process.env.NEXT_PUBLIC_COGNITO_REDIRECT_URI,
  logoutUri: process.env.NEXT_PUBLIC_COGNITO_LOGOUT_URI,
};

function requiredEnvironment(value: string | undefined, name: string): string {
  if (!value) {
    throw new Error(`${name} is required for Cognito authentication.`);
  }
  return value;
}

function getUserManager(): UserManager {
  if (typeof window === "undefined") {
    throw new Error("Cognito authentication is only available in the browser.");
  }

  if (!userManager) {
    userManager = new UserManager({
      authority: requiredEnvironment(
        cognitoEnvironment.issuer,
        "NEXT_PUBLIC_COGNITO_ISSUER",
      ),
      client_id: requiredEnvironment(
        cognitoEnvironment.clientId,
        "NEXT_PUBLIC_COGNITO_CLIENT_ID",
      ),
      redirect_uri: requiredEnvironment(
        cognitoEnvironment.redirectUri,
        "NEXT_PUBLIC_COGNITO_REDIRECT_URI",
      ),
      post_logout_redirect_uri: requiredEnvironment(
        cognitoEnvironment.logoutUri,
        "NEXT_PUBLIC_COGNITO_LOGOUT_URI",
      ),
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
