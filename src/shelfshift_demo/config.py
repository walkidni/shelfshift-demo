"""Server configuration facade."""

from typing import Literal

from fastapi import Request
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ShelfShift"
    app_tagline: str = "Developer toolkit for ecommerce catalog translation."
    brand_primary: str = "#18d9b6"
    brand_secondary: str = "#27c6f5"
    brand_ink: str = "#020b1a"
    debug: bool = False
    log_verbosity: Literal["low", "medium", "high", "extrahigh"] = "medium"
    rapidapi_key: str | None = None
    cors_allow_origins: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("cors_allow_origins", mode="before")
    @classmethod
    def _coerce_cors_allow_origins(cls, value: object) -> str:
        if isinstance(value, str):
            return value
        if isinstance(value, (list, tuple, set)):
            filtered = [str(entry).strip() for entry in value if str(entry).strip()]
            return ",".join(filtered) if filtered else "*"
        return "*"

    @property
    def cors_allow_origins_list(self) -> tuple[str, ...]:
        entries = tuple(part.strip() for part in self.cors_allow_origins.split(",") if part.strip())
        return entries or ("*",)


def get_settings() -> Settings:
    return Settings()


def get_app_settings(request: Request) -> Settings:
    app_settings = getattr(request.app.state, "settings", None)
    if isinstance(app_settings, Settings):
        return app_settings
    return get_settings()


__all__ = ["Settings", "get_app_settings", "get_settings"]
