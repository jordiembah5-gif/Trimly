# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # General
    PROJECT_NAME: str = "Trimly API"
    VERSION: str = "1.0.0"

    # Database
    DATABASE_URL: str

    # Auth / JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days — keeps users logged in

    # Business rule constants (centralized so nothing is hardcoded later)
    MIN_BOOKING_GAP_HOURS: int = 3
    MAX_BOOKINGS_PER_BARBER_PER_DAY: int = 2

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()