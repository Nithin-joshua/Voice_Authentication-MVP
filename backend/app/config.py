import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Voice Authentication System"
    ENV = os.getenv("ENV", "development")

    # Database
    POSTGRES_URL = os.getenv(
        "POSTGRES_URL",
        "postgresql://postgres:postgres123@localhost:5432/voice_auth"
    )

    # Redis
    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    # Authentication
    MFCC_COUNT = 13
    AUTH_THRESHOLD = 0.85

settings = Settings()
