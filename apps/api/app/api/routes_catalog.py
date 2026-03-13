from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.domain import ResortEntry, TrailEntry


router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/trails")
async def list_trails(db: AsyncSession = Depends(get_db)) -> list[dict]:
    trails = (await db.execute(select(TrailEntry).order_by(TrailEntry.region, TrailEntry.name))).scalars().all()
    return [
        {
            "id": trail.id,
            "name": trail.name,
            "region": trail.region,
            "terrain": trail.terrain,
            "difficulty_score": trail.difficulty_score,
            "drive_time_hours": trail.drive_time_hours,
            "summary": trail.summary,
            "risks": trail.risks,
        }
        for trail in trails
    ]


@router.get("/resorts")
async def list_resorts(db: AsyncSession = Depends(get_db)) -> list[dict]:
    resorts = (await db.execute(select(ResortEntry).order_by(ResortEntry.region, ResortEntry.name))).scalars().all()
    return [
        {
            "id": resort.id,
            "name": resort.name,
            "region": resort.region,
            "terrain_mix": resort.terrain_mix,
            "snow_bias": resort.snow_bias,
            "summary": resort.summary,
        }
        for resort in resorts
    ]


@router.get("/conditions")
async def list_conditions() -> list[dict]:
    return [
        {"mode": "offroad", "source": "seed", "detail": "Use local trail notes and recent user logs."},
        {"mode": "ski", "source": "seed", "detail": "Use catalog baseline until live conditions are approved."},
    ]

