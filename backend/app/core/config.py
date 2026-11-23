from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Находим путь к корню репозитория (.env лежит в корне или в папке backend)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            ROOT_DIR / ".env",
            ROOT_DIR.parent / ".env",
            ".env",
            "../.env",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Projet2"
    environment: str = "local"
    database_url: str = "postgresql+psycopg://quizai:change-me-local-only@localhost:5432/quizai_db"
    secret_key: str = "default_fallback_secret_key"

settings = Settings()
