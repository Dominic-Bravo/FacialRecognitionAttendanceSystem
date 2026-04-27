from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Realtime API"
    debug: bool = False
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    ws_max_message_bytes: int = 65_536


@lru_cache
def get_settings() -> Settings:
    return Settings()
