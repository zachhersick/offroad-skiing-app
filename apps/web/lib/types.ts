import type { AgentRunSummary, Mode, PlannerRequestPayload, RecommendationOption } from "@terrainpilot/shared";

export type { AgentRunSummary, Mode, PlannerRequestPayload, RecommendationOption };

export interface DashboardSnapshot {
  profile: {
    display_name: string;
    mode: Mode;
    home_region: string;
    comfort_rating: number;
  };
  vehicles: Array<{ id: string; name: string; drivetrain: string; tire_size_inches: number }>;
  ski_quivers: Array<{ id: string; name: string; skis: Array<{ name: string; waist_mm: number }> }>;
  runs: AgentRunSummary[];
}

export interface ArtifactRecord {
  id: string;
  artifact_type: string;
  payload: Record<string, unknown>;
}

