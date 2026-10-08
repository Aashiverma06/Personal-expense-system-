import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "peis-insecure-secret-key-change-in-production-2026")
    DATABASE_PATH = os.environ.get("DATABASE_PATH", str(BASE_DIR / "peis.db"))
    MODEL_PATH = os.environ.get("MODEL_PATH", str(BASE_DIR / "app" / "data" / "trained_model.joblib"))
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_PATH = str(BASE_DIR / "test_peis.db")
    DEBUG = True

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
