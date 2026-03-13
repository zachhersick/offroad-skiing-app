from __future__ import annotations

from urllib.parse import urlparse

import httpx

from ..policies import ToolPolicyEngine
from .base import ToolContext


class HttpTool:
    name = "http"

    def __init__(self, policy: ToolPolicyEngine) -> None:
        self.policy = policy

    async def get_json(self, context: ToolContext, url: str) -> dict:
        host = urlparse(url).netloc
        result = self.policy.evaluate(self.name, "get", host)
        if result.decision == "deny":
            raise PermissionError(result.reason)
        if result.decision == "require_approval" and not context.approved:
            raise PermissionError(result.reason)
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

