from __future__ import annotations

import asyncio
import subprocess
from pathlib import Path

from .base import ToolContext


class PythonSandboxTool:
    name = "python_sandbox"

    async def run_snippet(self, context: ToolContext, code: str) -> subprocess.CompletedProcess[str]:
        script_path = Path(context.workspace) / "sandbox.py"
        script_path.write_text(code)
        process = await asyncio.create_subprocess_exec(
            "python",
            str(script_path),
            cwd=str(context.workspace),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=10)
        return subprocess.CompletedProcess(
            args=["python", str(script_path)],
            returncode=process.returncode,
            stdout=stdout.decode(),
            stderr=stderr.decode(),
        )

