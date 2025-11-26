from typing import Optional

import httpx

from .config import settings


class ScrapClient:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or settings.base_url
        self.session = httpx.Client(base_url=self.base_url, follow_redirects=True)

    def login(self) -> bool:
        """Ejemplo de login: ajustar al formulario real."""
        payload = {
            "username": settings.username,
            "password": settings.password,
        }
        resp = self.session.post("/login", data=payload)
        return resp.is_success

    def get(self, path: str, **kwargs):
        return self.session.get(path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.session.post(path, **kwargs)

    def close(self):
        self.session.close()
