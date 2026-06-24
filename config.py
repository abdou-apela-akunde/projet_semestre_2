"""Configuration partagee par toute l'application."""

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    """Configuration centralisée de l'application."""

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    DEBUG = FLASK_ENV == "development"
    ANNEE_DEBUT = 2015
    ANNEE_FIN = 2023
    ANNEES = list(range(ANNEE_FIN, ANNEE_DEBUT - 1, -1))

    LOCAL_SQLITE_PATH = BASE_DIR / "data" / "sae201_local.db"
    SEED_SQL_PATH = BASE_DIR / "data" / "sae204_ideal.sql"

    @classmethod
    def annee_valide(cls, annee):
        """Indique si une annee est disponible dans le projet."""
        return annee in cls.ANNEES

    @classmethod
    def db_url(cls):
        """Construit l'URL SQLAlchemy pour MySQL ou SQLite local."""
        """Construit l'URL SQLAlchemy, avec SQLite local si MySQL n'est pas configuré."""
        if cls.DB_USER and cls.DB_PASSWORD and cls.DB_HOST and cls.DB_NAME:
            return (
                f"mysql+pymysql://{cls.DB_USER}:{cls.DB_PASSWORD}"
                f"@{cls.DB_HOST}/{cls.DB_NAME}"
            )
        return f"sqlite:///{cls.LOCAL_SQLITE_PATH.as_posix()}"
