from __future__ import annotations

import asyncio
from pathlib import Path

from ..policies import ToolPolicyEngine
from .base import ToolContext


class ShellCommandTool:
    name = "shell_command"
    allowed_commands = {"echo", "ls"}

    def __init__(self, policy: ToolPolicyEngine) -> None:
        self.policy = policy

    async def run(self, context: ToolContext, command: list[str]) -> tuple[int, str, str]:
        if not command or command[0] not in self.allowed_commands:
            raise PermissionError("command is not allowlisted")
        result = self.policy.evaluate(self.name, "run", command[0])
        if result.decision == "require_approval" and not context.approved:
            raise PermissionError(result.reason)
        process = await asyncio.create_subprocess_exec(
            *command,
            cwd=str(Path(context.workspace)),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return process.returncode, stdout.decode(), stderr.decode()

