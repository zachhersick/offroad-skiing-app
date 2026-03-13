from __future__ import annotations

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agent_core import AgentRuntime, PlannerExecutionContext
from agent_core.policies import ToolPolicyEngine
from app.core.config import get_settings
from app.models.domain import (
    AgentRun,
    AgentStatus,
    Approval,
    ApprovalStatus,
    Artifact,
    ArtifactType,
    PackingList,
    Profile,
    Recommendation,
    ResortEntry,
    SkiQuiver,
    StepLog,
    StepType,
    TrailEntry,
    Trip,
    TripStatus,
    Vehicle,
)
from app.schemas.planner import PlannerRequest


def _model_to_dict(instance: object, fields: list[str]) -> dict:
    return {field: getattr(instance, field) for field in fields}


async def create_trip_and_run(session: AsyncSession, user_id: str, payload: PlannerRequest) -> AgentRun:
    trip = Trip(
        user_id=user_id,
        mode=payload.mode,
        title=payload.title,
        region=payload.region,
        objective=payload.objective,
        status=TripStatus.draft,
        planner_input=payload.model_dump(),
    )
    session.add(trip)
    await session.flush()
    run = AgentRun(
        user_id=user_id,
        trip_id=trip.id,
        mode=payload.mode,
        title=payload.title,
        status=AgentStatus.queued,
        request_payload=payload.model_dump(),
    )
    session.add(run)
    await session.commit()
    await session.refresh(run)
    return run


async def enqueue_run(redis: Redis, run_id: str) -> None:
    await redis.rpush("terrainpilot:planner_runs", run_id)


async def process_run(session: AsyncSession, run_id: str) -> AgentRun:
    run = await session.get(AgentRun, run_id)
    if run is None:
        raise ValueError("run not found")

    run.status = AgentStatus.planning
    await session.flush()

    trail_catalog = [
        _model_to_dict(
            row,
            ["id", "name", "region", "terrain", "difficulty_score", "drive_time_hours", "summary", "risks", "metadata"],
        )
        for row in (await session.execute(select(TrailEntry))).scalars().all()
    ]
    resort_catalog = [
        _model_to_dict(row, ["id", "name", "region", "terrain_mix", "snow_bias", "summary", "metadata"])
        for row in (await session.execute(select(ResortEntry))).scalars().all()
    ]
    profile = (
        await session.execute(select(Profile).where(Profile.user_id == run.user_id))
    ).scalar_one_or_none()
    vehicle = None
    ski_quiver = None
    if run.request_payload.get("owned_vehicle_id"):
        vehicle = await session.get(Vehicle, run.request_payload["owned_vehicle_id"])
    if run.request_payload.get("owned_ski_quiver_id"):
        ski_quiver = await session.get(SkiQuiver, run.request_payload["owned_ski_quiver_id"])

    runtime = AgentRuntime(
        ToolPolicyEngine(
            live_http_enabled=get_settings().enable_live_http,
            approved_hosts=get_settings().approved_http_hosts_list,
        )
    )
    context = PlannerExecutionContext(
        run_id=run.id,
        mode=run.mode.value,
        request=run.request_payload,
        profile=_model_to_dict(
            profile,
            [
                "id",
                "display_name",
                "mode",
                "home_region",
                "comfort_rating",
                "max_drive_time_hours",
                "preferred_terrain",
                "snow_preference",
                "park_powder_bias",
                "details",
            ],
        )
        if profile
        else {},
        vehicle=_model_to_dict(
            vehicle,
            ["id", "name", "drivetrain", "lift_inches", "tire_size_inches", "armor_notes", "recovery_gear", "notes"],
        )
        if vehicle
        else {},
        ski_quiver=_model_to_dict(ski_quiver, ["id", "name", "skis", "notes"]) if ski_quiver else {},
        trail_catalog=trail_catalog,
        resort_catalog=resort_catalog,
    )

    plan = runtime.plan(context)
    session.add(Artifact(agent_run_id=run.id, artifact_type=ArtifactType.plan, payload=plan.model_dump()))
    session.add(
        StepLog(
            agent_run_id=run.id,
            step_order=1,
            step_type=StepType.analyze_request,
            status="completed",
            message="Planner generated a bounded execution plan.",
            payload=plan.model_dump(),
        )
    )

    run.status = AgentStatus.executing
    recommendation, checklist, execution, approval_artifact = runtime.execute(context)
    session.add(Artifact(agent_run_id=run.id, artifact_type=ArtifactType.recommendation, payload=recommendation.model_dump()))
    session.add(Artifact(agent_run_id=run.id, artifact_type=ArtifactType.checklist, payload=checklist.model_dump()))
    session.add(Artifact(agent_run_id=run.id, artifact_type=ArtifactType.execution, payload=execution.model_dump()))

    session.add(
        StepLog(
            agent_run_id=run.id,
            step_order=2,
            step_type=StepType.score_options,
            status="completed",
            message="Executor produced recommendation artifacts.",
            payload=recommendation.model_dump(),
        )
    )

    if approval_artifact and approval_artifact.required:
        session.add(Artifact(agent_run_id=run.id, artifact_type=ArtifactType.approval, payload=approval_artifact.model_dump()))
        session.add(
            Approval(
                agent_run_id=run.id,
                action=approval_artifact.action,
                reason=approval_artifact.reason,
                status=ApprovalStatus.pending,
                context=approval_artifact.context,
            )
        )
        run.status = AgentStatus.approval_required
        await session.commit()
        return run

    run.status = AgentStatus.reviewing
    review = runtime.review(context, recommendation, checklist)
    if not review.passed and run.retry_count < 1:
        run.retry_count += 1
        if context.mode == "offroad" and context.trail_catalog:
            context.trail_catalog = context.trail_catalog[1:]
        elif context.mode == "ski" and context.ski_quiver:
            skis = list(context.ski_quiver.get("skis", []))
            context.ski_quiver["skis"] = skis[1:]
        recommendation, checklist, execution, _ = runtime.execute(context)
        review = runtime.review(context, recommendation, checklist)
        session.add(
            StepLog(
                agent_run_id=run.id,
                step_order=3,
                step_type=StepType.compile_checklist,
                status="retried",
                message="Reviewer requested one selective retry.",
                payload={"retry_count": run.retry_count},
            )
        )
        session.add(Artifact(agent_run_id=run.id, artifact_type=ArtifactType.recommendation, payload=recommendation.model_dump()))
        session.add(Artifact(agent_run_id=run.id, artifact_type=ArtifactType.checklist, payload=checklist.model_dump()))
        session.add(Artifact(agent_run_id=run.id, artifact_type=ArtifactType.execution, payload=execution.model_dump()))
    session.add(Artifact(agent_run_id=run.id, artifact_type=ArtifactType.review, payload=review.model_dump()))
    session.add(
        StepLog(
            agent_run_id=run.id,
            step_order=4,
            step_type=StepType.review_output,
            status="completed" if review.passed else "failed",
            message=review.summary,
            payload=review.model_dump(),
        )
    )

    if review.passed:
        run.status = AgentStatus.completed
        trip = await session.get(Trip, run.trip_id)
        if trip:
            trip.status = TripStatus.planned
        session.add(PackingList(trip_id=run.trip_id, title=checklist.title, items=[item.model_dump() for item in checklist.items]))
        session.add(Recommendation(trip_id=run.trip_id, mode=run.mode, payload=recommendation.model_dump()))
    else:
        run.status = AgentStatus.failed

    await session.commit()
    await session.refresh(run)
    return run


async def serialize_run_artifacts(session: AsyncSession, run_id: str) -> list[dict]:
    rows = (await session.execute(select(Artifact).where(Artifact.agent_run_id == run_id))).scalars().all()
    return [{"id": row.id, "artifact_type": row.artifact_type.value, "payload": row.payload} for row in rows]


async def serialize_run_logs(session: AsyncSession, run_id: str) -> list[dict]:
    rows = (await session.execute(select(StepLog).where(StepLog.agent_run_id == run_id))).scalars().all()
    return [
        {
            "id": row.id,
            "step_order": row.step_order,
            "step_type": row.step_type.value,
            "status": row.status,
            "message": row.message,
            "payload": row.payload,
        }
        for row in rows
    ]


async def record_approval_decision(session: AsyncSession, run_id: str, approved: bool) -> AgentRun:
    approval = (
        await session.execute(select(Approval).where(Approval.agent_run_id == run_id).order_by(Approval.created_at.desc()))
    ).scalars().first()
    if approval is None:
        raise ValueError("approval not found")
    approval.status = ApprovalStatus.approved if approved else ApprovalStatus.rejected
    run = await session.get(AgentRun, run_id)
    if run is None:
        raise ValueError("run not found")
    run.status = AgentStatus.queued if approved else AgentStatus.failed
    if approved:
        run.request_payload = {**run.request_payload, "live_conditions_approved": True}
    session.add(
        StepLog(
            agent_run_id=run_id,
            step_order=4,
            step_type=StepType.await_approval,
            status="approved" if approved else "rejected",
            message="User resolved the approval request.",
            payload={"approved": approved},
        )
    )
    await session.commit()
    await session.refresh(run)
    return run
