import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from .config import settings

ASSETS_DIR = Path(settings.output_dir) / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def save_json(name: str, records: Iterable[Dict[str, Any]]):
    path = Path(settings.output_dir) / f"{name}.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(list(records), f, ensure_ascii=False, indent=2)
    return path


def save_html(name: str, html: str):
    path = Path(settings.output_dir) / f"{name}.html"
    path.write_text(html, encoding="utf-8")
    return path


def _build_asset_path(abs_url: str) -> Path:
    parsed = urlparse(abs_url)
    rel_path = parsed.path.lstrip("/") or "index"
    return ASSETS_DIR / rel_path


def download_assets(html: str, client) -> List[Tuple[str, Path]]:
    """
    Descarga CSS/JS/IMG referenciados en el HTML y los guarda en data/raw/assets.
    No borra archivos existentes.
    """
    soup = BeautifulSoup(html, "html.parser")
    tags_attrs = [("link", "href"), ("script", "src"), ("img", "src")]
    assets: List[Tuple[str, Path]] = []
    seen = set()

    for tag, attr in tags_attrs:
        for node in soup.find_all(tag):
            url = node.get(attr)
            if not url or url.startswith("data:"):
                continue
            abs_url = urljoin(client.base_url, url)
            if abs_url in seen:
                continue
            seen.add(abs_url)

            asset_path = _build_asset_path(abs_url)
            asset_path.parent.mkdir(parents=True, exist_ok=True)

            if asset_path.exists():
                assets.append((abs_url, asset_path))
                continue

            try:
                resp = client.session.get(abs_url)
                if resp.is_success:
                    asset_path.write_bytes(resp.content)
                    assets.append((abs_url, asset_path))
            except Exception:
                continue

    return assets
