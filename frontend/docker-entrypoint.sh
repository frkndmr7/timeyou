#!/bin/sh
set -eu

node <<'NODE'
const fs = require("node:fs");

const values = {
  cognitoIssuer: process.env.NEXT_PUBLIC_COGNITO_ISSUER,
  cognitoClientId: process.env.NEXT_PUBLIC_COGNITO_CLIENT_ID,
  cognitoRedirectUri: process.env.NEXT_PUBLIC_COGNITO_REDIRECT_URI,
  cognitoLogoutUri: process.env.NEXT_PUBLIC_COGNITO_LOGOUT_URI,
  apiBaseUrl: process.env.NEXT_PUBLIC_API_BASE_URL,
  analyticsApiBaseUrl: process.env.NEXT_PUBLIC_ANALYTICS_API_BASE_URL,
};

for (const [name, value] of Object.entries(values)) {
  if (!value) {
    throw new Error(`Missing runtime public configuration: ${name}`);
  }
}

fs.mkdirSync("/app/public", { recursive: true });
fs.writeFileSync(
  "/app/public/runtime-config.js",
  `window.TIMEYOU_CONFIG = ${JSON.stringify(values)};\n`,
);
NODE

exec "$@"
