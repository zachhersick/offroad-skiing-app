from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


Mode = Literal["offroad", "ski"]
ArtifactType = Literal["plan", "recommendation", "checklist", "review", "approval", "execution"]


class PlannedStep(BaseModel):
    order: int
    step_type: Literal["analyze_request", "score_options", "compile_checklist", "review_output", "await_approval"]
    title: str
    description: str
    required_inputs: list[str] = Field(default_factory=list)


class PlanArtifact(BaseModel):
    artifact_type: Literal["plan"] = "plan"
    summary: str
    mode: Mode
    steps: list[PlannedStep]
    assumptions: list[str] = Field(default_factory=list)


class RecommendationOption(BaseModel):
    title: str
    score: float
    summary: str
    reasons: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class RecommendationArtifact(BaseModel):
    artifact_type: Literal["recommendation"] = "recommendation"
    mode: Mode
    primary_recommendation: str
    ranked_options: list[RecommendationOption]
    notes: list[str] = Field(default_factory=list)


class ChecklistItem(BaseModel):
    label: str
    category: str
    required: bool = True
    rationale: str


class ChecklistArtifact(BaseModel):
    artifact_type: Literal["checklist"] = "checklist"
    mode: Mode
    title: str
    items: list[ChecklistItem]


class ExecutionArtifact(BaseModel):
    artifact_type: Literal["execution"] = "execution"
    completed_steps: list[str]
    skipped_steps: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    outputs: dict[str, Any] = Field(default_factory=dict)


class ReviewIssue(BaseModel):
    severity: Literal["low", "medium", "high"]
    message: str
    suggested_fix: str


class ReviewArtifact(BaseModel):
    artifact_type: Literal["review"] = "review"
    passed: bool
    score: float
    summary: str
    issues: list[ReviewIssue] = Field(default_factory=list)
    retry_step_orders: list[int] = Field(default_factory=list)


class ApprovalArtifact(BaseModel):
    artifact_type: Literal["approval"] = "approval"
    action: str
    reason: str
    required: bool = True
    status: Literal["pending", "approved", "rejected"] = "pending"
    context: dict[str, Any] = Field(default_factory=dict)

