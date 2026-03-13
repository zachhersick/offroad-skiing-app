from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


Mode = Literal["offroad", "ski"]


class ProfileUpdate(BaseModel):
    display_name: str
    mode: Mode
    home_region: str
    comfort_rating: int = Field(default=3, ge=1, le=5)
    max_drive_time_hours: int = Field(default=4, ge=1, le=12)
    preferred_terrain: list[str] = Field(default_factory=list)
    snow_preference: str | None = None
    park_powder_bias: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class VehicleCreate(BaseModel):
    name: str
    drivetrain: str
    lift_inches: float = 0
    tire_size_inches: int = 30
    armor_notes: str | None = None
    recovery_gear: dict[str, Any] = Field(default_factory=dict)
    notes: str | None = None


class SkiQuiverCreate(BaseModel):
    name: str
    skis: list[dict[str, Any]] = Field(default_factory=list)
    notes: str | None = None


class GearItemCreate(BaseModel):
    mode: Mode
    category: str
    name: str
    notes: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

