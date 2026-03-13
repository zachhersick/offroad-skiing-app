from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    type_annotation_map = {dict[str, object]: JSON}


class Mode(str, enum.Enum):
    offroad = "offroad"
    ski = "ski"


class TripStatus(str, enum.Enum):
    draft = "draft"
    planned = "planned"
    completed = "completed"


class GearCategory(str, enum.Enum):
    safety = "safety"
    recovery = "recovery"
    apparel = "apparel"
    camping = "camping"
    ski = "ski"
    vehicle = "vehicle"


class AgentStatus(str, enum.Enum):
    queued = "queued"
    planning = "planning"
    executing = "executing"
    reviewing = "reviewing"
    approval_required = "approval_required"
    completed = "completed"
    failed = "failed"


class StepType(str, enum.Enum):
    analyze_request = "analyze_request"
    score_options = "score_options"
    compile_checklist = "compile_checklist"
    await_approval = "await_approval"
    review_output = "review_output"


class ApprovalStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ArtifactType(str, enum.Enum):
    plan = "plan"
    recommendation = "recommendation"
    checklist = "checklist"
    review = "review"
    approval = "approval"
    execution = "execution"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


def uuid_pk() -> Mapped[str]:
    return mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[str] = uuid_pk()
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False)


class Profile(TimestampMixin, Base):
    __tablename__ = "profiles"

    id: Mapped[str] = uuid_pk()
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True)
    display_name: Mapped[str] = mapped_column(String(120))
    mode: Mapped[Mode] = mapped_column(Enum(Mode))
    home_region: Mapped[str] = mapped_column(String(120))
    comfort_rating: Mapped[int] = mapped_column(Integer, default=3)
    max_drive_time_hours: Mapped[int] = mapped_column(Integer, default=4)
    preferred_terrain: Mapped[list[str]] = mapped_column(JSON, default=list)
    snow_preference: Mapped[str | None] = mapped_column(String(50), nullable=True)
    park_powder_bias: Mapped[str | None] = mapped_column(String(50), nullable=True)
    details: Mapped[dict] = mapped_column(JSON, default=dict)

    user: Mapped[User] = relationship(back_populates="profile")


class Vehicle(TimestampMixin, Base):
    __tablename__ = "vehicles"

    id: Mapped[str] = uuid_pk()
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    drivetrain: Mapped[str] = mapped_column(String(20))
    lift_inches: Mapped[float] = mapped_column(Float, default=0)
    tire_size_inches: Mapped[int] = mapped_column(Integer, default=30)
    armor_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    recovery_gear: Mapped[dict] = mapped_column(JSON, default=dict)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class SkiQuiver(TimestampMixin, Base):
    __tablename__ = "ski_quivers"

    id: Mapped[str] = uuid_pk()
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    skis: Mapped[list[dict]] = mapped_column(JSON, default=list)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class GearItem(TimestampMixin, Base):
    __tablename__ = "gear_items"

    id: Mapped[str] = uuid_pk()
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    mode: Mapped[Mode] = mapped_column(Enum(Mode))
    category: Mapped[GearCategory] = mapped_column(Enum(GearCategory))
    name: Mapped[str] = mapped_column(String(120))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)


class Trip(TimestampMixin, Base):
    __tablename__ = "trips"

    id: Mapped[str] = uuid_pk()
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    mode: Mapped[Mode] = mapped_column(Enum(Mode))
    title: Mapped[str] = mapped_column(String(160))
    region: Mapped[str] = mapped_column(String(120))
    objective: Mapped[str] = mapped_column(Text)
    status: Mapped[TripStatus] = mapped_column(Enum(TripStatus), default=TripStatus.draft)
    planner_input: Mapped[dict] = mapped_column(JSON, default=dict)


class Route(TimestampMixin, Base):
    __tablename__ = "routes"

    id: Mapped[str] = uuid_pk()
    trip_id: Mapped[str] = mapped_column(ForeignKey("trips.id"), index=True)
    name: Mapped[str] = mapped_column(String(160))
    waypoints: Mapped[list[dict]] = mapped_column(JSON, default=list)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class TrailEntry(TimestampMixin, Base):
    __tablename__ = "trail_entries"

    id: Mapped[str] = uuid_pk()
    name: Mapped[str] = mapped_column(String(160), unique=True)
    region: Mapped[str] = mapped_column(String(120))
    terrain: Mapped[str] = mapped_column(String(80))
    difficulty_score: Mapped[int] = mapped_column(Integer)
    drive_time_hours: Mapped[int] = mapped_column(Integer)
    summary: Mapped[str] = mapped_column(Text)
    risks: Mapped[list[str]] = mapped_column(JSON, default=list)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)


class ResortEntry(TimestampMixin, Base):
    __tablename__ = "resort_entries"

    id: Mapped[str] = uuid_pk()
    name: Mapped[str] = mapped_column(String(160), unique=True)
    region: Mapped[str] = mapped_column(String(120))
    terrain_mix: Mapped[str] = mapped_column(String(80))
    snow_bias: Mapped[str] = mapped_column(String(80))
    summary: Mapped[str] = mapped_column(Text)
    metadata: Mapped[dict] = mapped_column(JSON, default=dict)


class Condition(TimestampMixin, Base):
    __tablename__ = "conditions"

    id: Mapped[str] = uuid_pk()
    mode: Mapped[Mode] = mapped_column(Enum(Mode))
    source_type: Mapped[str] = mapped_column(String(40))
    source_id: Mapped[str] = mapped_column(String(36), index=True)
    details: Mapped[dict] = mapped_column(JSON, default=dict)


class PackingList(TimestampMixin, Base):
    __tablename__ = "packing_lists"

    id: Mapped[str] = uuid_pk()
    trip_id: Mapped[str] = mapped_column(ForeignKey("trips.id"), index=True)
    title: Mapped[str] = mapped_column(String(160))
    items: Mapped[list[dict]] = mapped_column(JSON, default=list)


class Recommendation(TimestampMixin, Base):
    __tablename__ = "recommendations"

    id: Mapped[str] = uuid_pk()
    trip_id: Mapped[str] = mapped_column(ForeignKey("trips.id"), index=True)
    mode: Mapped[Mode] = mapped_column(Enum(Mode))
    payload: Mapped[dict] = mapped_column(JSON, default=dict)


class AgentRun(TimestampMixin, Base):
    __tablename__ = "agent_runs"

    id: Mapped[str] = uuid_pk()
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    trip_id: Mapped[str] = mapped_column(ForeignKey("trips.id"), index=True)
    mode: Mapped[Mode] = mapped_column(Enum(Mode))
    title: Mapped[str] = mapped_column(String(160))
    status: Mapped[AgentStatus] = mapped_column(Enum(AgentStatus), default=AgentStatus.queued)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    request_payload: Mapped[dict] = mapped_column(JSON, default=dict)


class StepLog(TimestampMixin, Base):
    __tablename__ = "step_logs"

    id: Mapped[str] = uuid_pk()
    agent_run_id: Mapped[str] = mapped_column(ForeignKey("agent_runs.id"), index=True)
    step_order: Mapped[int] = mapped_column(Integer)
    step_type: Mapped[StepType] = mapped_column(Enum(StepType))
    status: Mapped[str] = mapped_column(String(40))
    message: Mapped[str] = mapped_column(Text)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)


class Artifact(TimestampMixin, Base):
    __tablename__ = "artifacts"

    id: Mapped[str] = uuid_pk()
    agent_run_id: Mapped[str] = mapped_column(ForeignKey("agent_runs.id"), index=True)
    artifact_type: Mapped[ArtifactType] = mapped_column(Enum(ArtifactType))
    payload: Mapped[dict] = mapped_column(JSON, default=dict)


class Approval(TimestampMixin, Base):
    __tablename__ = "approvals"

    id: Mapped[str] = uuid_pk()
    agent_run_id: Mapped[str] = mapped_column(ForeignKey("agent_runs.id"), index=True)
    action: Mapped[str] = mapped_column(String(120))
    reason: Mapped[str] = mapped_column(Text)
    status: Mapped[ApprovalStatus] = mapped_column(Enum(ApprovalStatus), default=ApprovalStatus.pending)
    context: Mapped[dict] = mapped_column(JSON, default=dict)
