from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

APP_NAME = os.getenv("APP_NAME", "SIIS-UÍGE")
APP_ENV = os.getenv("APP_ENV", "development")
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
CLIENT_SERVER_URL = os.getenv("CLIENT_SERVER_URL", "http://127.0.0.1:8000")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://siis_user:change_me@localhost:5432/siis_uige")
SECRET_KEY = os.getenv("SECRET_KEY", "development-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
