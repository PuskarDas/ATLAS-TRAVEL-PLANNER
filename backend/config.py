from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Application settings and configuration."""

    # Application
    app_name: str = "AI-Group-Travel-Planner"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"

    # Server
    server_host: str = "0.0.0.0"
    server_port: int = 8000

    # Database
    database_type: str = "mysql"
    database_url: str = (
        "mysql+pymysql://user:password@localhost:3306/travel_planner"
    )
    mongodb_url: Optional[str] = None

    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # API Keys
    google_maps_api_key: Optional[str] = None
    openweather_api_key: Optional[str] = None
    opentripmap_api_key: Optional[str] = None
    skyscanner_api_key: Optional[str] = None
    hotel_api_key: Optional[str] = None

    # CORS
    cors_origins: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    # Email
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from_email: str = "noreply@travelplanner.com"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"

    # Frontend
    frontend_url: str = "http://localhost:3000"

    # ML Models
    model_path: str = "./ml_models/"
    recommendation_model: str = "recommendation_model.pkl"
    nlp_model: str = "nlp_model.pkl"
    clustering_model: str = "clustering_model.pkl"

    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"

    model_config = SettingsConfigDict(
        env_file=_BACKEND_DIR / ".env",
        env_prefix="TRAVEL_",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
