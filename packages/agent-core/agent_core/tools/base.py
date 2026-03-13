from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class ToolContext:
    run_id: str
    workspace: Path
    approved: bool = False
    metadata: dict[str, str] = field(default_factory=dict)

