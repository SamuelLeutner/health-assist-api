from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str
    SECRET_KEY: str = Field(min_length=32)
    ALGORITHM: Literal["HS256", "HS384", "HS512"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(gt=0)
    DATABASE_URL: str

    CORS_ORIGINS: str = "http://localhost:3000"

    ZAP_API_URL: str = "http://127.0.0.1:8080"
    TARGET_API: str = "http://host.docker.internal:8000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()
        ]


settings = Settings()