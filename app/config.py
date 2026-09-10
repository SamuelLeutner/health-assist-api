from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str

    CORS_ORIGINS: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()
        ]


settings = Settings()
