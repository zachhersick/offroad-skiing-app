from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _normalize_database_url(url: str) -> str:
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)
    return url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = Field(default="development", alias="APP_ENV")
    database_url: str = Field(default="sqlite+aiosqlite:///./terrainpilot.db", alias="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    jwt_secret: str = Field(default="dev-secret", alias="JWT_SECRET")
    jwt_refresh_secret: str = Field(default="dev-refresh-secret", alias="JWT_REFRESH_SECRET")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_base_url: str = Field(default="https://api.openai.com/v1", alias="OPENAI_BASE_URL")
    openai_model: str = Field(default="gpt-5-mini", alias="OPENAI_MODEL")
    enable_live_http: bool = Field(default=False, alias="ENABLE_LIVE_HTTP")
    approved_http_hosts: str = Field(default="api.open-meteo.com", alias="APPROVED_HTTP_HOSTS")
    cors_origins: str = Field(default="http://localhost:3000", alias="CORS_ORIGINS")
    run_inline_agent_jobs: bool = Field(default=False, alias="RUN_INLINE_AGENT_JOBS")

    @property
    def approved_http_hosts_list(self) -> list[str]:
        return [item.strip() for item in self.approved_http_hosts.split(",") if item.strip()]

    @property
    def cors_origins_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

    @property
    def sqlalchemy_database_url(self) -> str:
        return _normalize_database_url(self.database_url)


@lru_cache
def get_settings() -> Settings:
    return Settings()
