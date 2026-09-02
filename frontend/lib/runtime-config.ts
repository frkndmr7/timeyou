export type RuntimeConfig = {
  cognitoIssuer: string;
  cognitoClientId: string;
  cognitoRedirectUri: string;
  cognitoLogoutUri: string;
  apiBaseUrl: string;
  analyticsApiBaseUrl: string;
};

declare global {
  interface Window {
    TIMEYOU_CONFIG?: RuntimeConfig;
  }
}

function required(value: unknown, name: keyof RuntimeConfig): string {
  if (typeof value !== "string" || value.length === 0) {
    throw new Error(`Runtime configuration field ${name} is required.`);
  }
  return value;
}

export function getRuntimeConfig(): RuntimeConfig {
  if (typeof window === "undefined") {
    throw new Error("Runtime configuration is only available in the browser.");
  }

  const config = window.TIMEYOU_CONFIG;
  if (!config) {
    throw new Error("Runtime configuration has not loaded.");
  }

  return {
    cognitoIssuer: required(config.cognitoIssuer, "cognitoIssuer"),
    cognitoClientId: required(config.cognitoClientId, "cognitoClientId"),
    cognitoRedirectUri: required(config.cognitoRedirectUri, "cognitoRedirectUri"),
    cognitoLogoutUri: required(config.cognitoLogoutUri, "cognitoLogoutUri"),
    apiBaseUrl: required(config.apiBaseUrl, "apiBaseUrl"),
    analyticsApiBaseUrl: required(config.analyticsApiBaseUrl, "analyticsApiBaseUrl"),
  };
}
