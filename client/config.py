from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SERVER_URL = os.getenv("CLIENT_SERVER_URL", "http://127.0.0.1:8000")
APP_TITLE = "SIIS-UÍGE"
