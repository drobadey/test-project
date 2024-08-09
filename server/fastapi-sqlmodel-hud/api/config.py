import os
import secrets
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # these are passed to things like the FastAPI() constructor.
    PROJECT_NAME: str = f"SQLModel API - {os.getenv('ENV', 'development').capitalize()}"
    DESCRIPTION: str = "A RestAPI for access HMIS data"
    ENV: Literal["development", "staging", "production"] = "development"
    VERSION: str = "0.1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # TODO: The following should come from a .env.production or .env.development
    #  ... or better from a keystore!
    DATABASE_URI: str = "postgresql+psycopg2://postgres:postgres@0.0.0.0:5432/hmisdb"
    API_USERNAME: str = "api_user"
    API_PASSWORD: str = "ASuperStrongPassword!"
    # NOTE: server ip and port is controlled by agsi.py (local native dev) and Dockerfile (dockerdev)

    class Config:
        case_sensitive = True


settings = Settings()


class TestSettings(Settings):
    class Config:
        case_sensitive = True


test_settings = TestSettings()
