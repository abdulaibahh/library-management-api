from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Limkokwing Library Management API"
    environment: str = "development"
    debug: bool = True
    database_url: str = "postgresql+asyncpg://user:password@localhost/library_db"
    jwt_secret_key: str = "CHANGE_ME"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
