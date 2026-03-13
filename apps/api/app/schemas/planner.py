from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


Mode = Literal["offroad", "ski"]


class PlannerRequest(BaseModel):
    mode: Mode
    title: str
    region: str
    objective: str
    duration_hours: int = Field(ge=1, le=72)
    experience_level: str
    preferences: list[str] = Field(default_factory=list)
    special_constraints: list[str] = Field(default_factory=list)
    owned_vehicle_id: str | None = None
    owned_ski_quiver_id: str | None = None
    refresh_live_conditions: bool = False


class PlannerRunResponse(BaseModel):
    id: str
    trip_id: str
    status: str
    title: str


class ArtifactResponse(BaseModel):
    id: str
    artifact_type: str
    payload: dict[str, Any]

