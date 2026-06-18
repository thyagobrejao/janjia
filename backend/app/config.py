import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    PROJECT_NAME: str = "JanjIA"
    ENV: str = "development"
    ALLOWED_ORIGINS: List[str] = Field(default=["http://localhost:8080"])

    # Backend/JWT
    SECRET_KEY: str = Field(default="janjia_super_secret_jwt_key_2026_laugh_out_loud")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Initial Admin Creds
    ADMIN_USERNAME: str = "admin"
    ADMIN_EMAIL: EmailStr = "admin@janjia.com"
    ADMIN_PASSWORD: str = "admin_senha_secreta_123"

    # PostgreSQL
    POSTGRES_SERVER: str = "postgres"
    POSTGRES_USER: str = "janjia_user"
    POSTGRES_PASSWORD: str = "janjia_password"
    POSTGRES_DB: str = "janjia_db"
    POSTGRES_PORT: int = 5432

    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Ollama
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "qwen3:8b"
    OLLAMA_TIMEOUT: int = 60
    OLLAMA_MAX_RETRIES: int = 3

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 20

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
