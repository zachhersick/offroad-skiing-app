from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_auth import router as auth_router
from app.api.routes_approvals import router as approvals_router
from app.api.routes_catalog import router as catalog_router
from app.api.routes_planner import router as planner_router
from app.api.routes_profile import router as profile_router
from app.api.routes_trips import router as trips_router
from app.core.config import get_settings
from app.db.base import Base
from app.db.seed import seed_catalog
from app.db.session import SessionLocal, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with SessionLocal() as session:
        await seed_catalog(session)
    yield


app = FastAPI(title="TerrainPilot API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(approvals_router)
app.include_router(profile_router)
app.include_router(catalog_router)
app.include_router(planner_router)
app.include_router(trips_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
