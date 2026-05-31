from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "postgresql+psycopg://tradepulse:tradepulse@postgres:5432/tradepulse"
    redis_url: str = "redis://redis:6379/0"
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    clerk_jwks_url: str | None = None
    sentry_dsn: str | None = None
    openai_api_key: str | None = None
    alpha_vantage_api_key: str | None = None
    newsapi_key: str | None = None
    fmp_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
