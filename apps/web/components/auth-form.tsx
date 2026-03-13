"use client";

import { useState, useTransition } from "react";

const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function postAuth(path: "signup" | "signin", body: Record<string, unknown>) {
  const response = await fetch(`${apiBase}/auth/${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    credentials: "include"
  });
  if (!response.ok) {
    throw new Error(`${path} failed`);
  }
  return response.json();
}

export function AuthForm() {
  const [mode, setMode] = useState<"signup" | "signin">("signup");
  const [result, setResult] = useState<string>("No active session");
  const [isPending, startTransition] = useTransition();

  function handleSubmit(formData: FormData) {
    const payload =
      mode === "signup"
        ? {
            email: String(formData.get("email")),
            password: String(formData.get("password")),
            display_name: String(formData.get("displayName")),
            mode: String(formData.get("primaryMode")),
            home_region: String(formData.get("homeRegion"))
          }
        : {
            email: String(formData.get("email")),
            password: String(formData.get("password"))
          };

    startTransition(async () => {
      try {
        const response = await postAuth(mode, payload);
        setResult(`Signed in as ${response.email}`);
      } catch {
        setResult("API unavailable, auth form is ready for the live backend.");
      }
    });
  }

  return (
    <section className="rounded-[2rem] border border-white/10 bg-shale/70 p-6 shadow-terrain backdrop-blur">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-frost/70">Authentication</p>
          <h2 className="mt-2 font-display text-3xl text-white">Create a TerrainPilot workspace</h2>
        </div>
        <div className="inline-flex rounded-full border border-white/15 bg-white/5 p-1">
          {(["signup", "signin"] as const).map((value) => (
            <button
              key={value}
              type="button"
              onClick={() => setMode(value)}
              className={`rounded-full px-4 py-2 text-sm ${mode === value ? "bg-sand text-shale" : "text-frost/80"}`}
            >
              {value}
            </button>
          ))}
        </div>
      </div>
      <form key={mode} action={handleSubmit} className="mt-6 grid gap-4 md:grid-cols-2">
        <label className="grid gap-2">
          <span className="text-sm text-frost/80">Email</span>
          <input name="email" type="email" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white" />
        </label>
        <label className="grid gap-2">
          <span className="text-sm text-frost/80">Password</span>
          <input name="password" type="password" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white" />
        </label>
        {mode === "signup" ? (
          <>
            <label className="grid gap-2">
              <span className="text-sm text-frost/80">Display name</span>
              <input name="displayName" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white" />
            </label>
            <label className="grid gap-2">
              <span className="text-sm text-frost/80">Home region</span>
              <input name="homeRegion" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white" />
            </label>
            <label className="grid gap-2 md:col-span-2">
              <span className="text-sm text-frost/80">Primary mode</span>
              <select name="primaryMode" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white">
                <option value="offroad">Off-Road</option>
                <option value="ski">Ski</option>
              </select>
            </label>
          </>
        ) : null}
        <div className="md:col-span-2 flex items-center justify-between rounded-3xl bg-white/5 px-4 py-4">
          <p className="text-sm text-frost/80">{result}</p>
          <button
            type="submit"
            disabled={isPending}
            className="rounded-full bg-canyon px-6 py-3 text-sm font-semibold text-white disabled:opacity-60"
          >
            {isPending ? "Working..." : mode === "signup" ? "Create account" : "Sign in"}
          </button>
        </div>
      </form>
    </section>
  );
}

