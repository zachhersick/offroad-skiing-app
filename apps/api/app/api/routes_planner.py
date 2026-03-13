from __future__ import annotations

from redis.asyncio import Redis
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.db.session import get_db
from app.models.domain import AgentRun, Approval, User
from app.schemas.planner import PlannerRequest, PlannerRunResponse
from app.services.planner import (
    create_trip_and_run,
    enqueue_run,
    process_run,
    record_approval_decision,
    serialize_run_artifacts,
    serialize_run_logs,
)


router = APIRouter(prefix="/planner", tags=["planner"])


class ApprovalDecision(BaseModel):
    approved: bool


@router.post("/runs", response_model=PlannerRunResponse)
async def submit_run(payload: PlannerRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> PlannerRunResponse:
    settings = get_settings()
    run = await create_trip_and_run(db, user.id, payload)
    if settings.run_inline_agent_jobs:
        run = await process_run(db, run.id)
    else:
        redis = Redis.from_url(settings.redis_url)
        await enqueue_run(redis, run.id)
        await redis.aclose()
    return PlannerRunResponse(id=run.id, trip_id=run.trip_id, status=run.status.value, title=run.title)


@router.get("/runs")
async def list_runs(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> list[dict]:
    runs = (await db.execute(select(AgentRun).where(AgentRun.user_id == user.id).order_by(AgentRun.created_at.desc()))).scalars().all()
    return [
        {
            "id": run.id,
            "trip_id": run.trip_id,
            "title": run.title,
            "status": run.status.value,
            "mode": run.mode.value,
            "createdAt": run.created_at.isoformat(),
        }
        for run in runs
    ]


@router.get("/runs/{run_id}")
async def get_run(run_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> dict:
    run = await db.get(AgentRun, run_id)
    if run is None or run.user_id != user.id:
        raise HTTPException(status_code=404, detail="Run not found")
    approvals = (await db.execute(select(Approval).where(Approval.agent_run_id == run.id))).scalars().all()
    return {
        "id": run.id,
        "trip_id": run.trip_id,
        "title": run.title,
        "status": run.status.value,
        "mode": run.mode.value,
        "retry_count": run.retry_count,
        "approvals": [{"id": item.id, "action": item.action, "status": item.status.value} for item in approvals],
        "logs": await serialize_run_logs(db, run.id),
    }


@router.get("/runs/{run_id}/artifacts")
async def get_run_artifacts(run_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> list[dict]:
    run = await db.get(AgentRun, run_id)
    if run is None or run.user_id != user.id:
        raise HTTPException(status_code=404, detail="Run not found")
    return await serialize_run_artifacts(db, run.id)


@router.post("/runs/{run_id}/approve")
async def approve_run(run_id: str, payload: ApprovalDecision, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> dict:
    run = await db.get(AgentRun, run_id)
    if run is None or run.user_id != user.id:
        raise HTTPException(status_code=404, detail="Run not found")
    try:
        run = await record_approval_decision(db, run_id, payload.approved)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if payload.approved:
        settings = get_settings()
        if settings.run_inline_agent_jobs:
            run = await process_run(db, run.id)
        else:
            redis = Redis.from_url(settings.redis_url)
            await enqueue_run(redis, run.id)
            await redis.aclose()
    return {"id": run.id, "status": run.status.value}
