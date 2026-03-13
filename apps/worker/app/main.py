from __future__ import annotations

import asyncio

from redis.asyncio import Redis

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.services.planner import process_run


async def worker_loop() -> None:
    settings = get_settings()
    redis = Redis.from_url(settings.redis_url)
    while True:
        _, run_id = await redis.blpop("terrainpilot:planner_runs")
        async with SessionLocal() as session:
            await process_run(session, run_id.decode())


def main() -> None:
    asyncio.run(worker_loop())


if __name__ == "__main__":
    main()
