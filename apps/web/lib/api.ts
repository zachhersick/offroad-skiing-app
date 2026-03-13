import { dashboardSnapshot, sampleApprovals, sampleArtifacts, sampleTrips } from "./mock-data";
import type { ArtifactRecord, DashboardSnapshot, PlannerRequestPayload } from "./types";

const serverApiBase = process.env.INTERNAL_API_BASE_URL ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://api:8000";

async function apiFetch(path: string, init?: RequestInit) {
  if (typeof window === "undefined") {
    const { cookies } = await import("next/headers");
    const cookieStore = await cookies();
    const cookieHeader = cookieStore
      .getAll()
      .map((cookie) => `${cookie.name}=${cookie.value}`)
      .join("; ");
    return fetch(`${serverApiBase}${path}`, {
      ...init,
      headers: {
        ...(init?.headers ?? {}),
        ...(cookieHeader ? { cookie: cookieHeader } : {})
      },
      cache: "no-store"
    });
  }

  return fetch(`/api${path}`, {
    ...init,
    credentials: "include"
  });
}

export async function fetchDashboard(): Promise<DashboardSnapshot> {
  try {
    const response = await apiFetch("/planner/runs");
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
    const response = await apiFetch("/planner/runs", {
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
        owned_vehicle_id: payload.ownedVehicleId,
        owned_ski_quiver_id: payload.ownedSkiQuiverId,
        refresh_live_conditions: payload.refreshLiveConditions
      })
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
    const response = await apiFetch(`/planner/runs/${runId}/artifacts`);
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
    const response = await apiFetch("/trips");
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
    const response = await apiFetch("/approvals");
    if (!response.ok) {
      return sampleApprovals;
    }
    return response.json();
  } catch {
    return sampleApprovals;
  }
}
