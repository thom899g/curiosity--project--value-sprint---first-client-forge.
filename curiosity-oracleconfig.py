"""
Configuration settings for the Magnetic Oracle.
"""

import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    project_id: str = os.getenv("PROJECT_ID", "curiosity-oracle-prod")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    stripe_api_key: str = os.getenv("STRIPE_API_KEY", "")
    stripe_webhook_secret: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")

    # Firebase credentials
    firebase_credentials_path: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")

    class Config:
        env_file = ".env"

settings = Settings()