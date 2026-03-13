from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain import ResortEntry, TrailEntry


TRAIL_SEED = [
    {
        "name": "Otay Backbone",
        "region": "San Diego",
        "terrain": "desert",
        "difficulty_score": 3,
        "drive_time_hours": 2,
        "summary": "Rocky half-day route with good views and a moderate technical section.",
        "risks": ["Loose rock", "Narrow shelf section"],
        "details": {"best_for": ["stock-plus trucks", "half-day trips"]},
    },
    {
        "name": "Anza Wash Loop",
        "region": "Anza-Borrego",
        "terrain": "desert",
        "difficulty_score": 2,
        "drive_time_hours": 3,
        "summary": "Scenic wash route suited for mostly stock midsize vehicles.",
        "risks": ["Sand pockets"],
        "details": {"best_for": ["day trips", "scenic driving"]},
    },
    {
        "name": "Big Bear Ridge Connector",
        "region": "Big Bear",
        "terrain": "forest",
        "difficulty_score": 4,
        "drive_time_hours": 3,
        "summary": "Longer route with rocks, ruts, and weather sensitivity.",
        "risks": ["Snow closures", "Deep ruts"],
        "details": {"best_for": ["built rigs", "full-day trips"]},
    },
]

RESORT_SEED = [
    {
        "name": "Mammoth Mountain",
        "region": "Eastern Sierra",
        "terrain_mix": "all_mountain",
        "snow_bias": "storm",
        "summary": "Large alpine resort with strong storm and chalk performance.",
        "details": {"best_for": ["powder", "advanced all-mountain"]},
    },
    {
        "name": "Mt. Bachelor",
        "region": "Central Oregon",
        "terrain_mix": "mixed",
        "snow_bias": "wind_buff",
        "summary": "Volcanic terrain with strong visibility and mixed condition coverage.",
        "details": {"best_for": ["all-mountain", "spring laps"]},
    },
]


async def seed_catalog(session: AsyncSession) -> None:
    trail_count = len((await session.execute(select(TrailEntry))).scalars().all())
    if trail_count == 0:
        session.add_all(TrailEntry(**item) for item in TRAIL_SEED)
    resort_count = len((await session.execute(select(ResortEntry))).scalars().all())
    if resort_count == 0:
        session.add_all(ResortEntry(**item) for item in RESORT_SEED)
    await session.commit()
