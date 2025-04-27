from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str
    API_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Library Management System"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()