from __future__ import annotations

import requests

from client.config import SERVER_URL


class ApiClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or SERVER_URL).rstrip("/")

    def get(self, endpoint: str, timeout: int = 10):
        return requests.get(f"{self.base_url}{endpoint}", timeout=timeout)

    def post(self, endpoint: str, payload: dict, timeout: int = 10):
        return requests.post(f"{self.base_url}{endpoint}", json=payload, timeout=timeout)

    def ping(self):
        try:
            response = self.get("/health", timeout=5)
            return response.ok, response.json()
        except requests.RequestException as exc:
            return False, {"error": str(exc)}
