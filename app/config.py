"""
Configuration settings for the FastAPI GraphQL backend.
"""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database Configuration
    # Optional at load time; we populate from fallbacks if missing.
    database_url: Optional[str] = Field(None, env="DATABASE_URL")
    
    # Supabase Configuration (optional; not all deployments need API keys)
    supabase_url: Optional[str] = Field(None, env="SUPABASE_URL")
    supabase_anon_key: Optional[str] = Field(None, env="SUPABASE_ANON_KEY")
    supabase_service_role_key: Optional[str] = Field(None, env="SUPABASE_SERVICE_ROLE_KEY")
    
    # Application Configuration
    debug: bool = Field(False, env="DEBUG")
    environment: str = Field("development", env="ENVIRONMENT")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    # Server Configuration
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    
    # Security (for future authentication implementation)
    secret_key: Optional[str] = Field(None, env="SECRET_KEY")
    algorithm: str = Field("HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # CORS Configuration
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:8080",
        env="CORS_ORIGINS"
    )
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }


# Global settings instance
settings = Settings()

# Populate database_url from common Supabase/Vercel fallbacks if missing
if not settings.database_url:
    fallback_env_vars = [
        # Common alternates seen in Supabase/Vercel setups
        "SUPABASE_DB_URL",
        "SUPABASE_DATABASE_URL",
        "POSTGRES_URL",
        "POSTGRES_PRISMA_URL",
        "PG_DATABASE_URL",
        "DB_URL",
    ]
    for var_name in fallback_env_vars:
        env_val = os.getenv(var_name)
        if env_val:
            settings.database_url = env_val
            break


def get_settings() -> Settings:
    """Get the application settings."""
    return settings 