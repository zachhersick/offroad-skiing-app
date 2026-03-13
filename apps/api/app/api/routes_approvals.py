from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.domain import AgentRun, Approval, User


router = APIRouter(prefix="/approvals", tags=["approvals"])


@router.get("")
async def list_approvals(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> list[dict]:
    rows = (
        await db.execute(
            select(Approval, AgentRun)
            .join(AgentRun, AgentRun.id == Approval.agent_run_id)
            .where(AgentRun.user_id == user.id)
            .order_by(Approval.created_at.desc())
        )
    ).all()
    return [
        {
            "id": approval.id,
            "run_id": run.id,
            "title": run.title,
            "action": approval.action,
            "reason": approval.reason,
            "status": approval.status.value,
        }
        for approval, run in rows
    ]

