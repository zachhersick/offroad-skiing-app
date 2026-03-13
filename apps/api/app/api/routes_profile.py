from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.domain import GearCategory, GearItem, Profile, SkiQuiver, User, Vehicle
from app.schemas.domain import GearItemCreate, ProfileUpdate, SkiQuiverCreate, VehicleCreate


router = APIRouter(tags=["profile"])


@router.get("/profiles/me")
async def get_profile(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> dict:
    profile = (await db.execute(select(Profile).where(Profile.user_id == user.id))).scalar_one()
    return {
        "id": profile.id,
        "display_name": profile.display_name,
        "mode": profile.mode.value,
        "home_region": profile.home_region,
        "comfort_rating": profile.comfort_rating,
        "max_drive_time_hours": profile.max_drive_time_hours,
        "preferred_terrain": profile.preferred_terrain,
        "snow_preference": profile.snow_preference,
        "park_powder_bias": profile.park_powder_bias,
        "details": profile.details,
    }


@router.put("/profiles/me")
async def update_profile(payload: ProfileUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> dict:
    profile = (await db.execute(select(Profile).where(Profile.user_id == user.id))).scalar_one()
    for field, value in payload.model_dump().items():
        setattr(profile, field, value)
    await db.commit()
    await db.refresh(profile)
    return {"id": profile.id, "display_name": profile.display_name, "mode": profile.mode.value}


@router.get("/vehicles")
async def list_vehicles(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> list[dict]:
    vehicles = (await db.execute(select(Vehicle).where(Vehicle.user_id == user.id))).scalars().all()
    return [
        {
            "id": vehicle.id,
            "name": vehicle.name,
            "drivetrain": vehicle.drivetrain,
            "lift_inches": vehicle.lift_inches,
            "tire_size_inches": vehicle.tire_size_inches,
            "recovery_gear": vehicle.recovery_gear,
        }
        for vehicle in vehicles
    ]


@router.post("/vehicles")
async def create_vehicle(payload: VehicleCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> dict:
    vehicle = Vehicle(user_id=user.id, **payload.model_dump())
    db.add(vehicle)
    await db.commit()
    await db.refresh(vehicle)
    return {"id": vehicle.id, "name": vehicle.name}


@router.get("/ski-quivers")
async def list_ski_quivers(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> list[dict]:
    quivers = (await db.execute(select(SkiQuiver).where(SkiQuiver.user_id == user.id))).scalars().all()
    return [{"id": quiver.id, "name": quiver.name, "skis": quiver.skis} for quiver in quivers]


@router.post("/ski-quivers")
async def create_ski_quiver(payload: SkiQuiverCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> dict:
    quiver = SkiQuiver(user_id=user.id, **payload.model_dump())
    db.add(quiver)
    await db.commit()
    await db.refresh(quiver)
    return {"id": quiver.id, "name": quiver.name}


@router.get("/gear-items")
async def list_gear_items(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> list[dict]:
    items = (await db.execute(select(GearItem).where(GearItem.user_id == user.id))).scalars().all()
    return [{"id": item.id, "name": item.name, "category": item.category.value, "mode": item.mode.value} for item in items]


@router.post("/gear-items")
async def create_gear_item(payload: GearItemCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> dict:
    item = GearItem(
        user_id=user.id,
        mode=payload.mode,
        category=GearCategory(payload.category),
        name=payload.name,
        notes=payload.notes,
        details=payload.details,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return {"id": item.id, "name": item.name}
