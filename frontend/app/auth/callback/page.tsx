"use client";

import { useEffect, useState } from "react";

import { completeLogin } from "../../../lib/auth";

export default function AuthCallbackPage() {
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    completeLogin()
      .then(() => {
        window.location.replace("/");
      })
      .catch((reason: unknown) => {
        const message = reason instanceof Error ? reason.message : "Unknown callback error.";
        setError(`Login could not be completed: ${message}`);
      });
  }, []);

  return (
    <main>
      <h1>Signing in…</h1>
      {error && <p role="alert">{error}</p>}
    </main>
  );
}
