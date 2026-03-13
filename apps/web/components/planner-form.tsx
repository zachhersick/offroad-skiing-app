"use client";

import { useState, useTransition } from "react";

import { ModeSwitch } from "./mode-switch";
import { submitPlannerRequest } from "@/lib/api";
import { defaultPlannerRequest } from "@/lib/mock-data";
import type { PlannerRequestPayload } from "@/lib/types";

const offroadPlaceholder =
  "Plan a half-day trail run near San Diego for a mostly stock midsize truck with conservative lines.";
const skiPlaceholder =
  "Recommend my setup for a Mammoth storm day and build a checklist for a weekend trip.";

export function PlannerForm() {
  const [form, setForm] = useState<PlannerRequestPayload>(defaultPlannerRequest);
  const [runStatus, setRunStatus] = useState<string>("idle");
  const [isPending, startTransition] = useTransition();

  function handleSubmit(formData: FormData) {
    const payload: PlannerRequestPayload = {
      ...form,
      title: String(formData.get("title")),
      region: String(formData.get("region")),
      objective: String(formData.get("objective")),
      durationHours: Number(formData.get("durationHours")),
      experienceLevel: String(formData.get("experienceLevel")),
      preferences: String(formData.get("preferences"))
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean),
      specialConstraints: String(formData.get("specialConstraints"))
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean),
      refreshLiveConditions: Boolean(formData.get("refreshLiveConditions"))
    };
    startTransition(async () => {
      const response = await submitPlannerRequest(payload);
      setRunStatus(response.status);
    });
  }

  return (
    <section className="rounded-[2rem] border border-white/10 bg-shale/70 p-6 shadow-terrain backdrop-blur">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-frost/70">Planner Agent</p>
          <h2 className="mt-2 font-display text-3xl text-white">Build a trip plan with bounded agent runs</h2>
        </div>
        <ModeSwitch
          mode={form.mode}
          onChange={(mode) =>
            setForm((current) => ({
              ...current,
              mode,
              title: mode === "offroad" ? "Half-day desert trail" : "Storm day at Mammoth",
              objective: mode === "offroad" ? offroadPlaceholder : skiPlaceholder
            }))
          }
        />
      </div>
      <form key={form.mode} action={handleSubmit} className="mt-6 grid gap-4 lg:grid-cols-2">
        <label className="grid gap-2">
          <span className="text-sm text-frost/80">Trip title</span>
          <input
            name="title"
            defaultValue={form.title}
            className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none ring-0"
          />
        </label>
        <label className="grid gap-2">
          <span className="text-sm text-frost/80">Region</span>
          <input
            name="region"
            defaultValue={form.region}
            className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none ring-0"
          />
        </label>
        <label className="grid gap-2 lg:col-span-2">
          <span className="text-sm text-frost/80">Objective</span>
          <textarea
            name="objective"
            defaultValue={form.objective}
            rows={4}
            className="rounded-3xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none ring-0"
          />
        </label>
        <label className="grid gap-2">
          <span className="text-sm text-frost/80">Duration hours</span>
          <input
            name="durationHours"
            defaultValue={form.durationHours}
            type="number"
            min={1}
            max={72}
            className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none ring-0"
          />
        </label>
        <label className="grid gap-2">
          <span className="text-sm text-frost/80">Experience level</span>
          <input
            name="experienceLevel"
            defaultValue={form.experienceLevel}
            className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none ring-0"
          />
        </label>
        <label className="grid gap-2">
          <span className="text-sm text-frost/80">Preferences (comma-separated)</span>
          <input
            name="preferences"
            defaultValue={form.preferences.join(", ")}
            className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none ring-0"
          />
        </label>
        <label className="grid gap-2">
          <span className="text-sm text-frost/80">Constraints (comma-separated)</span>
          <input
            name="specialConstraints"
            defaultValue={form.specialConstraints.join(", ")}
            className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white outline-none ring-0"
          />
        </label>
        <label className="flex items-center gap-3 text-sm text-frost/80 lg:col-span-2">
          <input name="refreshLiveConditions" type="checkbox" className="size-4 rounded border-white/20 bg-white/5" />
          Request live condition refresh if approval is granted
        </label>
        <div className="lg:col-span-2 flex items-center justify-between rounded-3xl bg-white/5 px-4 py-4">
          <div>
            <p className="text-sm text-frost/80">Run status</p>
            <p className="font-display text-xl text-white">{runStatus}</p>
          </div>
          <button
            type="submit"
            disabled={isPending}
            className="rounded-full bg-canyon px-6 py-3 text-sm font-semibold text-white transition hover:bg-[#b46831] disabled:opacity-60"
          >
            {isPending ? "Submitting..." : "Run planner"}
          </button>
        </div>
      </form>
    </section>
  );
}
