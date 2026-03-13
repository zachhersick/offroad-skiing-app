export type Mode = "offroad" | "ski";

export type AgentStatus =
  | "queued"
  | "planning"
  | "executing"
  | "reviewing"
  | "approval_required"
  | "completed"
  | "failed";

export type ArtifactType =
  | "plan"
  | "recommendation"
  | "checklist"
  | "review"
  | "approval"
  | "execution";

export interface PlannerRequestPayload {
  mode: Mode;
  title: string;
  region: string;
  objective: string;
  durationHours: number;
  experienceLevel: string;
  preferences: string[];
  specialConstraints: string[];
  ownedVehicleId?: string;
  ownedSkiQuiverId?: string;
  refreshLiveConditions?: boolean;
}

export interface RecommendationOption {
  title: string;
  score: number;
  summary: string;
  reasons: string[];
  risks: string[];
}

export interface AgentRunSummary {
  id: string;
  title: string;
  mode: Mode;
  status: AgentStatus;
  createdAt: string;
}

export const modeLabels: Record<Mode, string> = {
  offroad: "Off-Road",
  ski: "Ski"
};

