import { dashboardSnapshot, sampleApprovals, sampleArtifacts, sampleTrips } from "./mock-data";
import type { ArtifactRecord, DashboardSnapshot, PlannerRequestPayload } from "./types";

const browserApiBase = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
const serverApiBase = process.env.INTERNAL_API_BASE_URL ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

function resolveBaseUrl() {
  return typeof window === "undefined" ? serverApiBase : browserApiBase;
}

export async function fetchDashboard(): Promise<DashboardSnapshot> {
  try {
    const response = await fetch(`${resolveBaseUrl()}/planner/runs`, {
      cache: "no-store",
      credentials: "include"
    });
    if (!response.ok) {
      return dashboardSnapshot;
    }
    const runs = await response.json();
    return { ...dashboardSnapshot, runs };
  } catch {
    return dashboardSnapshot;
  }
}

export async function submitPlannerRequest(payload: PlannerRequestPayload): Promise<{ id: string; status: string }> {
  try {
    const response = await fetch(`${resolveBaseUrl()}/planner/runs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        mode: payload.mode,
        title: payload.title,
        region: payload.region,
        objective: payload.objective,
        duration_hours: payload.durationHours,
        experience_level: payload.experienceLevel,
        preferences: payload.preferences,
        special_constraints: payload.specialConstraints,
        refresh_live_conditions: payload.refreshLiveConditions
      }),
      credentials: "include"
    });
    if (!response.ok) {
      throw new Error("Planner request failed");
    }
    return response.json();
  } catch {
    return { id: "local-preview", status: "preview" };
  }
}

export async function fetchArtifacts(runId: string): Promise<ArtifactRecord[]> {
  try {
    const response = await fetch(`${resolveBaseUrl()}/planner/runs/${runId}/artifacts`, {
      cache: "no-store",
      credentials: "include"
    });
    if (!response.ok) {
      return sampleArtifacts;
    }
    return response.json();
  } catch {
    return sampleArtifacts;
  }
}

export async function fetchTrips() {
  try {
    const response = await fetch(`${resolveBaseUrl()}/trips`, {
      cache: "no-store",
      credentials: "include"
    });
    if (!response.ok) {
      return sampleTrips;
    }
    return response.json();
  } catch {
    return sampleTrips;
  }
}

export async function fetchApprovals() {
  try {
    const response = await fetch(`${resolveBaseUrl()}/approvals`, {
      cache: "no-store",
      credentials: "include"
    });
    if (!response.ok) {
      return sampleApprovals;
    }
    return response.json();
  } catch {
    return sampleApprovals;
  }
}
