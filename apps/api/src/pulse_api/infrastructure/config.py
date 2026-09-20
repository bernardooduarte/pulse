from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://pulse:pulse@localhost:5436/pulse"
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
