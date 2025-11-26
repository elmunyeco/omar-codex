import json
from pathlib import Path
from typing import Any, Dict, Iterable

from .config import settings


def save_json(name: str, records: Iterable[Dict[str, Any]]):
    path = Path(settings.output_dir) / f"{name}.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(list(records), f, ensure_ascii=False, indent=2)
    return path


def save_html(name: str, html: str):
    path = Path(settings.output_dir) / f"{name}.html"
    path.write_text(html, encoding="utf-8")
    return path
