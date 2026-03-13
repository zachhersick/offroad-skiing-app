from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from .artifacts.models import (
    ApprovalArtifact,
    ChecklistArtifact,
    ChecklistItem,
    ExecutionArtifact,
    PlanArtifact,
    PlannedStep,
    RecommendationArtifact,
    RecommendationOption,
    ReviewArtifact,
    ReviewIssue,
)
from .policies import ToolPolicyEngine


@dataclass(slots=True)
class PlannerExecutionContext:
    run_id: str
    mode: str
    request: dict
    profile: dict | None = None
    vehicle: dict | None = None
    ski_quiver: dict | None = None
    trail_catalog: list[dict] = field(default_factory=list)
    resort_catalog: list[dict] = field(default_factory=list)


class AgentRuntime:
    def __init__(self, policy_engine: ToolPolicyEngine) -> None:
        self.policy_engine = policy_engine

    def plan(self, context: PlannerExecutionContext) -> PlanArtifact:
        steps = [
            PlannedStep(
                order=1,
                step_type="analyze_request",
                title="Analyze planning request",
                description="Normalize intent, constraints, and owned setup.",
                required_inputs=["planner_request", "profile"],
            ),
            PlannedStep(
                order=2,
                step_type="score_options",
                title="Score destination options",
                description="Rank trails or ski setups using the structured heuristics.",
                required_inputs=["catalog", "owned_setup"],
            ),
            PlannedStep(
                order=3,
                step_type="compile_checklist",
                title="Build checklist",
                description="Generate a trip-specific checklist with safety coverage.",
                required_inputs=["preferences", "conditions"],
            ),
            PlannedStep(
                order=4,
                step_type="review_output",
                title="Review for completeness",
                description="Validate recommendation quality and missing critical items.",
                required_inputs=["recommendation", "checklist"],
            ),
        ]
        if context.request.get("refresh_live_conditions") and not context.request.get("live_conditions_approved"):
            steps.insert(
                3,
                PlannedStep(
                    order=4,
                    step_type="await_approval",
                    title="Request approval for live conditions refresh",
                    description="External HTTP access requires approval before live condition retrieval.",
                    required_inputs=["approval"],
                ),
            )
            steps[-1].order = 5
        return PlanArtifact(
            summary=f"Create a {context.mode} trip plan for {context.request['title']}.",
            mode=context.mode,  # type: ignore[arg-type]
            steps=steps,
            assumptions=["Seed catalog data is current enough for a first-pass recommendation."],
        )

    def execute(self, context: PlannerExecutionContext) -> tuple[RecommendationArtifact, ChecklistArtifact, ExecutionArtifact, ApprovalArtifact | None]:
        approval = None
        if context.request.get("refresh_live_conditions") and not context.request.get("live_conditions_approved"):
            decision = self.policy_engine.evaluate("http", "get", "api.open-meteo.com")
            approval = ApprovalArtifact(
                action="refresh_live_conditions",
                reason=decision.reason,
                required=decision.decision == "require_approval",
                context={"host": "api.open-meteo.com"},
            )
            if approval.required:
                recommendation = RecommendationArtifact(
                    mode=context.mode,  # type: ignore[arg-type]
                    primary_recommendation="Awaiting approval before fetching live conditions.",
                    ranked_options=[],
                    notes=["The run paused before executing the live HTTP step."],
                )
                checklist = ChecklistArtifact(mode=context.mode, title="Pending approval checklist", items=[])
                execution = ExecutionArtifact(
                    completed_steps=["analyze_request", "score_options"],
                    skipped_steps=["compile_checklist"],
                    warnings=["Approval required for external HTTP access."],
                    outputs={"approval_required": True},
                )
                return recommendation, checklist, execution, approval

        if context.mode == "offroad":
            options = self._score_trails(context)
            checklist = self._build_offroad_checklist(context, options[0] if options else None)
        else:
            options = self._score_skis(context)
            checklist = self._build_ski_checklist(context, options[0] if options else None)
        recommendation = RecommendationArtifact(
            mode=context.mode,  # type: ignore[arg-type]
            primary_recommendation=options[0].title if options else "No suitable option available",
            ranked_options=options,
            notes=[
                "TerrainPilot favors conservative recommendations when setup capability is close to the route requirement.",
                "Live conditions were not fetched unless approval was granted.",
            ],
        )
        execution = ExecutionArtifact(
            completed_steps=["analyze_request", "score_options", "compile_checklist"],
            warnings=[],
            outputs={"top_option": recommendation.primary_recommendation},
        )
        return recommendation, checklist, execution, approval

    def review(self, context: PlannerExecutionContext, recommendation: RecommendationArtifact, checklist: ChecklistArtifact) -> ReviewArtifact:
        issues: list[ReviewIssue] = []
        if not recommendation.ranked_options:
            issues.append(
                ReviewIssue(
                    severity="high",
                    message="No recommendation options were generated.",
                    suggested_fix="Review the catalog filters and user setup inputs.",
                )
            )
        required_categories = {"navigation", "safety"}
        if context.mode == "offroad":
            required_categories.add("recovery")
        else:
            required_categories.add("snow")
        present_categories = {item.category for item in checklist.items}
        for category in sorted(required_categories - present_categories):
            issues.append(
                ReviewIssue(
                    severity="medium",
                    message=f"Checklist is missing the {category} category.",
                    suggested_fix="Regenerate the packing checklist with the missing safety grouping.",
                )
            )
        if context.mode == "offroad" and context.vehicle and recommendation.ranked_options:
            top_required = recommendation.ranked_options[0].metadata.get("required_capability", 0)
            vehicle_capability = self._vehicle_capability(context.vehicle)
            if vehicle_capability < top_required:
                issues.append(
                    ReviewIssue(
                        severity="high",
                        message="Top trail recommendation exceeds the recorded vehicle capability.",
                        suggested_fix="Recommend easier trails or require a better-equipped vehicle.",
                    )
                )
        passed = not any(issue.severity == "high" for issue in issues)
        return ReviewArtifact(
            passed=passed,
            score=max(0.0, 1.0 - 0.2 * len(issues)),
            summary="Review complete." if passed else "Review found issues requiring attention.",
            issues=issues,
            retry_step_orders=[2, 3] if issues else [],
        )

    def _score_trails(self, context: PlannerExecutionContext) -> list[RecommendationOption]:
        profile = context.profile or {}
        vehicle = context.vehicle or {}
        max_drive_time = int(profile.get("max_drive_time_hours", 6))
        capability = self._vehicle_capability(vehicle)
        scored: list[RecommendationOption] = []
        for entry in context.trail_catalog:
            difficulty = int(entry.get("difficulty_score", 1))
            terrain_match = 12 if entry.get("terrain") in (profile.get("preferred_terrain") or []) else 6
            comfort_buffer = max(0, 10 - abs(int(profile.get("comfort_rating", 3)) - difficulty) * 3)
            drive_penalty = max(0, (int(entry.get("drive_time_hours", 0)) - max_drive_time) * 4)
            capability_penalty = max(0, (difficulty * 18) - capability)
            score = max(1.0, 90 + terrain_match + comfort_buffer - drive_penalty - capability_penalty)
            scored.append(
                RecommendationOption(
                    title=entry["name"],
                    score=round(score, 2),
                    summary=entry["summary"],
                    reasons=[
                        f"Terrain fit: {entry['terrain']}",
                        f"Drive time: {entry['drive_time_hours']} hours",
                        f"Vehicle capability score: {capability}",
                    ],
                    risks=entry.get("risks", []),
                    metadata={"required_capability": difficulty * 18, "difficulty_score": difficulty},
                )
            )
        return sorted(scored, key=lambda item: item.score, reverse=True)[:3]

    def _score_skis(self, context: PlannerExecutionContext) -> list[RecommendationOption]:
        quiver = context.ski_quiver or {}
        snow_preference = (context.profile or {}).get("snow_preference", "powder")
        scored: list[RecommendationOption] = []
        for ski in quiver.get("skis", []):
            waist = ski.get("waist_mm", 95)
            score = 70.0
            if snow_preference == "powder":
                score += max(0, waist - 95) * 0.6
            elif snow_preference == "slush":
                score += 15 if 90 <= waist <= 104 else 4
            else:
                score += 12 if 88 <= waist <= 102 else 6
            if ski.get("terrain_bias") == (context.profile or {}).get("preferred_terrain"):
                score += 8
            scored.append(
                RecommendationOption(
                    title=ski["name"],
                    score=round(score, 2),
                    summary=ski.get("notes", "Versatile quiver option"),
                    reasons=[f"Waist width: {waist}mm", f"Snow preference: {snow_preference}"],
                    risks=["Verify tune and edge condition before the trip."],
                )
            )
        return sorted(scored, key=lambda item: item.score, reverse=True)[:3]

    def _build_offroad_checklist(self, context: PlannerExecutionContext, top_option: RecommendationOption | None) -> ChecklistArtifact:
        items = [
            ChecklistItem(label="Offline route map", category="navigation", rationale="Trail cell service can drop quickly."),
            ChecklistItem(label="Paper backup route notes", category="navigation", rationale="Recovery planning should survive device failure."),
            ChecklistItem(label="First aid kit", category="safety", rationale="Baseline trip safety."),
            ChecklistItem(label="Warm layer and water", category="safety", rationale="Weather can change even on a half-day trip."),
            ChecklistItem(label="Recovery strap", category="recovery", rationale="Basic self-recovery coverage."),
            ChecklistItem(label="Tire repair kit", category="recovery", rationale="Common field repair item."),
        ]
        if context.vehicle and not context.vehicle.get("recovery_gear", {}).get("traction_boards"):
            items.append(
                ChecklistItem(
                    label="Traction boards",
                    category="recovery",
                    required=False,
                    rationale="Recommended upgrade for a mostly stock vehicle on variable terrain.",
                )
            )
        if top_option:
            items.append(
                ChecklistItem(
                    label=f"Terrain notes for {top_option.title}",
                    category="planning",
                    required=True,
                    rationale="Review trail-specific obstacles before departure.",
                )
            )
        return ChecklistArtifact(mode="offroad", title="Off-road trip checklist", items=items)

    def _build_ski_checklist(self, context: PlannerExecutionContext, top_option: RecommendationOption | None) -> ChecklistArtifact:
        items = [
            ChecklistItem(label="Lift pass and ID", category="navigation", rationale="Required for resort access."),
            ChecklistItem(label="Helmet and goggles", category="safety", rationale="Baseline snow safety coverage."),
            ChecklistItem(label="Gloves and dry layers", category="snow", rationale="Adapt to changing mountain temps."),
            ChecklistItem(label="Wax and scraper", category="snow", required=False, rationale="Helpful for changing conditions."),
        ]
        if top_option:
            items.append(
                ChecklistItem(
                    label=f"Bindings and tune check for {top_option.title}",
                    category="planning",
                    rationale="Confirm the chosen setup is ready the night before.",
                )
            )
        return ChecklistArtifact(mode="ski", title="Ski day checklist", items=items)

    def _vehicle_capability(self, vehicle: dict) -> int:
        capability = 30
        if vehicle.get("drivetrain") in {"4wd", "awd"}:
            capability += 18
        lift_inches = float(vehicle.get("lift_inches", 0))
        tire_size = int(vehicle.get("tire_size_inches", 30))
        capability += int(lift_inches * 4)
        capability += max(0, tire_size - 30) * 3
        recovery = vehicle.get("recovery_gear", {})
        capability += 6 if recovery.get("winch") else 0
        capability += 4 if recovery.get("rear_locker") else 0
        return capability
