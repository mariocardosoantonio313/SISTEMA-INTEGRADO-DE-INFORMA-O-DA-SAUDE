from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import DATABASE_URL

FALLBACK_SQLITE_URL = "sqlite:///siis_uige_dev.db"

engine_url = DATABASE_URL
if os.getenv("USE_SQLITE_FALLBACK", "1") == "1" and DATABASE_URL.startswith("postgresql"):
    engine_url = FALLBACK_SQLITE_URL

engine = create_engine(engine_url, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
