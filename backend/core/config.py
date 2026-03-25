"""
Configuration settings for the Multi-Agent RFP System.

This module defines all configuration parameters using Pydantic settings
with environment variable support for different deployment environments.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    
    All settings can be overridden using environment variables with
    the same name (case-insensitive).
    """
    
    # Application Settings
    APP_NAME: str = "Multi-Agent RFP System"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_HOSTS: str = "*"
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # Database Settings (SQLite for demo without Docker)
    DATABASE_URL: str = "sqlite+aiosqlite:///./rfp_system.db"
    DATABASE_ECHO: bool = False
    
    # Redis Settings (In-memory fallback for demo)
    REDIS_URL: str = "memory://"
    REDIS_PASSWORD: Optional[str] = None
    
    # Message Queue Settings (In-memory fallback)
    CELERY_BROKER_URL: str = "memory://"
    CELERY_RESULT_BACKEND: str = "memory://"
    
    # Agent Configuration
    RFP_MONITORING_INTERVAL: int = 300  # 5 minutes
    MAX_CONCURRENT_RFPS: int = 10
    AGENT_TIMEOUT: int = 300  # 5 minutes
    
    # External API Settings
    COMMODITY_API_KEY: Optional[str] = None
    COMMODITY_API_URL: str = "https://api.commodities-api.com/v1"
    
    # ML/NLP Settings
    SPACY_MODEL: str = "en_core_web_sm"
    TRANSFORMERS_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    ML_MODEL_CACHE_DIR: str = "./models"
    
    # Web Scraping Settings
    SCRAPING_USER_AGENT: str = "RFP-Agent/1.0"
    SCRAPING_DELAY: float = 1.0
    MAX_SCRAPING_WORKERS: int = 5
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # File Storage Settings
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES: str = ".pdf,.doc,.docx,.txt"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()


def get_database_url() -> str:
    """Get the database URL for SQLAlchemy."""
    return settings.DATABASE_URL


def get_redis_url() -> str:
    """Get the Redis URL for connection."""
    return settings.REDIS_URL


def is_development() -> bool:
    """Check if running in development mode."""
    return settings.DEBUG


def is_production() -> bool:
    """Check if running in production mode."""
    return not settings.DEBUG


def get_allowed_hosts() -> List[str]:
    """Get allowed hosts as a list."""
    return [host.strip() for host in settings.ALLOWED_HOSTS.split(",")]


def get_cors_origins() -> List[str]:
    """Get CORS origins as a list."""
    return [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]


def get_allowed_file_types() -> List[str]:
    """Get allowed file types as a list."""
    return [ext.strip() for ext in settings.ALLOWED_FILE_TYPES.split(",")]