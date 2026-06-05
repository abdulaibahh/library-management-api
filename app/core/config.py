from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Limkokwing Library Management API"
    environment: str = "development"
    debug: bool = True

    # Prefer a full DATABASE_URL when provided (e.g. sqlite+aiosqlite:///./dev.db)
    DATABASE_URL: Optional[str] = None

    # Legacy individual DB settings (optional when DATABASE_URL is provided)
    DATABASE_HOST: Optional[str] = None
    DATABASE_PORT: Optional[int] = None
    DATABASE_NAME: Optional[str] = None
    DATABASE_USER: Optional[str] = None
    DATABASE_PASSWORD: Optional[str] = None

    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @property
    def database_url(self) -> str:
        # If a full DATABASE_URL is set in env, use it. Otherwise build Postgres URL from components.
        if self.DATABASE_URL:
            return self.DATABASE_URL

        if self.DATABASE_HOST and self.DATABASE_USER and self.DATABASE_NAME:
            return (
                f"postgresql+asyncpg://"
                f"{self.DATABASE_USER}:"
                f"{self.DATABASE_PASSWORD or ''}@"
                f"{self.DATABASE_HOST}:"
                f"{self.DATABASE_PORT or 5432}/"
                f"{self.DATABASE_NAME}"
            )

        raise ValueError("No database configuration provided. Set DATABASE_URL or individual DB_* vars.")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()