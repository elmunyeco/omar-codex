from typing import Optional
from urllib.parse import urljoin

import httpx

from .config import settings


class ScrapClient:
    def __init__(self, base_url: Optional[str] = None):
        # base_url con barra final
        self.base_url = (base_url or settings.base_url).rstrip("/") + "/"
        self.session = httpx.Client(base_url=self.base_url, follow_redirects=True)

    def login(self) -> bool:
        """Si no hay LOGIN_PATH, se asume acceso público."""
        if not settings.login_path:
            return True

        # El formulario real usa campos "usuario" y "pass"
        payload = {
            "usuario": settings.username,
            "pass": settings.password,
        }
        login_url = urljoin(self.base_url, settings.login_path)
        resp = self.session.post(login_url, data=payload)
        return resp.is_success

    def get(self, path: str, **kwargs):
        url = urljoin(self.base_url, path)
        return self.session.get(url, **kwargs)

    def post(self, path: str, **kwargs):
        url = urljoin(self.base_url, path)
        return self.session.post(url, **kwargs)

    def close(self):
        self.session.close()
