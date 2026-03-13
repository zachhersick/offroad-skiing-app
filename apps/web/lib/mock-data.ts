import type { ArtifactRecord, DashboardSnapshot, PlannerRequestPayload } from "./types";

export const defaultPlannerRequest: PlannerRequestPayload = {
  mode: "offroad",
  title: "Half-day desert trail",
  region: "San Diego",
  objective: "Plan a conservative but interesting route for a mostly stock midsize truck.",
  durationHours: 5,
  experienceLevel: "Intermediate beginner",
  preferences: ["desert", "scenic", "day trip"],
  specialConstraints: ["mostly stock truck", "half day"],
  refreshLiveConditions: false
};

export const dashboardSnapshot: DashboardSnapshot = {
  profile: {
    display_name: "Zach",
    mode: "offroad",
    home_region: "Southern California",
    comfort_rating: 3
  },
  vehicles: [
    {
      id: "veh_1",
      name: "Midsize Trail Truck",
      drivetrain: "4wd",
      tire_size_inches: 33
    }
  ],
  ski_quivers: [
    {
      id: "quiver_1",
      name: "Storm + Daily Driver",
      skis: [
        { name: "112 Powder", waist_mm: 112 },
        { name: "99 All-Mountain", waist_mm: 99 }
      ]
    }
  ],
  runs: [
    {
      id: "run_seed",
      title: "Half-day desert trail",
      mode: "offroad",
      status: "completed",
      createdAt: new Date().toISOString()
    }
  ]
};

export const sampleArtifacts: ArtifactRecord[] = [
  {
    id: "art_plan",
    artifact_type: "plan",
    payload: {
      summary: "Create an off-road trip plan for a half-day desert trail.",
      steps: [
        { order: 1, title: "Analyze request" },
        { order: 2, title: "Score trail options" },
        { order: 3, title: "Build checklist" },
        { order: 4, title: "Review output" }
      ]
    }
  },
  {
    id: "art_recommendation",
    artifact_type: "recommendation",
    payload: {
      primary_recommendation: "Otay Backbone",
      ranked_options: [
        {
          title: "Otay Backbone",
          score: 92.4,
          summary: "Moderate route with scenic payoff."
        },
        {
          title: "Anza Wash Loop",
          score: 88.1,
          summary: "Easier scenic fallback."
        }
      ]
    }
  },
  {
    id: "art_checklist",
    artifact_type: "checklist",
    payload: {
      title: "Off-road trip checklist",
      items: [
        { label: "Offline route map", category: "navigation" },
        { label: "Recovery strap", category: "recovery" }
      ]
    }
  }
];

export const sampleTrips = [
  {
    id: "trip_1",
    title: "Half-day desert trail",
    mode: "offroad",
    region: "San Diego",
    objective: "Conservative scenic route for a mostly stock midsize truck.",
    status: "planned"
  },
  {
    id: "trip_2",
    title: "Mammoth storm day",
    mode: "ski",
    region: "Eastern Sierra",
    objective: "Pick the right ski and pack for cold storm laps.",
    status: "planned"
  }
] as const;

export const sampleApprovals = [
  {
    id: "approval_1",
    run_id: "run_seed",
    title: "Half-day desert trail",
    action: "refresh_live_conditions",
    reason: "External HTTP requests require human approval.",
    status: "pending"
  }
];
