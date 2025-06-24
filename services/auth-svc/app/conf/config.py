from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLITE_FILE: str = "db.sqlite3"

    JWT_SECRET: str = "pryvit"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_SECONDS: int = 3600

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )

    @property
    def DB_URL(self) -> str:
        return f"sqlite+aiosqlite:///{self.SQLITE_FILE}"

settings = Settings()
