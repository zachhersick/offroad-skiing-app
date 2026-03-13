from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.services.planner import process_run
from redis.asyncio import Redis


async def worker_loop() -> None:
    settings = get_settings()
    redis = Redis.from_url(settings.redis_url)
    while True:
        _, run_id = await redis.blpop("terrainpilot:planner_runs")
        async with SessionLocal() as session:
            await process_run(session, run_id.decode())


if __name__ == "__main__":
    asyncio.run(worker_loop())

