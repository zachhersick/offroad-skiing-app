from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.domain import PackingList, Recommendation, Trip, User


router = APIRouter(prefix="/trips", tags=["trips"])


@router.get("")
async def list_trips(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> list[dict]:
    trips = (await db.execute(select(Trip).where(Trip.user_id == user.id).order_by(Trip.created_at.desc()))).scalars().all()
    return [
        {
            "id": trip.id,
            "title": trip.title,
            "mode": trip.mode.value,
            "region": trip.region,
            "objective": trip.objective,
            "status": trip.status.value,
        }
        for trip in trips
    ]


@router.get("/{trip_id}")
async def get_trip(trip_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> dict:
    trip = await db.get(Trip, trip_id)
    if trip is None or trip.user_id != user.id:
        raise HTTPException(status_code=404, detail="Trip not found")
    packing_lists = (await db.execute(select(PackingList).where(PackingList.trip_id == trip.id))).scalars().all()
    recommendations = (await db.execute(select(Recommendation).where(Recommendation.trip_id == trip.id))).scalars().all()
    return {
        "id": trip.id,
        "title": trip.title,
        "mode": trip.mode.value,
        "region": trip.region,
        "objective": trip.objective,
        "status": trip.status.value,
        "planner_input": trip.planner_input,
        "packing_lists": [{"id": item.id, "title": item.title, "items": item.items} for item in packing_lists],
        "recommendations": [{"id": item.id, "payload": item.payload} for item in recommendations],
    }

