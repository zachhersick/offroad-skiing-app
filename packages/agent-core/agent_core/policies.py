from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PolicyDecision = Literal["allow", "deny", "require_approval"]


@dataclass(slots=True)
class PolicyResult:
    decision: PolicyDecision
    reason: str


class ToolPolicyEngine:
    def __init__(self, live_http_enabled: bool, approved_hosts: list[str] | None = None) -> None:
        self.live_http_enabled = live_http_enabled
        self.approved_hosts = set(approved_hosts or [])

    def evaluate(self, tool_name: str, action: str, target: str = "") -> PolicyResult:
        if tool_name == "filesystem":
            return PolicyResult("allow", "ephemeral run workspace only")
        if tool_name == "python_sandbox":
            return PolicyResult("allow", "sandboxed execution allowed")
        if tool_name == "http":
            if not self.live_http_enabled:
                return PolicyResult("deny", "live HTTP is disabled")
            if target and target not in self.approved_hosts:
                return PolicyResult("deny", f"{target} is not allowlisted")
            return PolicyResult("require_approval", "external HTTP requests require human approval")
        if tool_name == "shell_command":
            return PolicyResult("require_approval", "shell access is approval-gated")
        return PolicyResult("deny", f"unsupported tool: {tool_name}:{action}")

