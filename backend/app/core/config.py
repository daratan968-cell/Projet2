from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )
    
    app_name: str = "Projet2"
    environment: str = "local"
    database_url: str = "postgresql+psycopg://localhost:5432/db"
    secret_key: str = "default_fallback_secret_key"

settings = Settings()
