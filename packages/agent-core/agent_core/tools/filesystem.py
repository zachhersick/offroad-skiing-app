from __future__ import annotations

from pathlib import Path

from .base import ToolContext


class FilesystemTool:
    name = "filesystem"

    def write_text(self, context: ToolContext, relative_path: str, content: str) -> Path:
        target = (context.workspace / relative_path).resolve()
        if context.workspace.resolve() not in target.parents and target != context.workspace.resolve():
            raise PermissionError("filesystem tool cannot escape the run workspace")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        return target

