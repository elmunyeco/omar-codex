from typing import List, Dict, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from ..client import ScrapClient
from .. import pipelines
from ..config import settings


def scrape_pacientes(client: ScrapClient, max_pages: Optional[int] = None) -> List[Dict]:
    """
    Descarga hasta max_pages páginas de pacientes, guardando HTML y assets.
    No borra nada y persiste cada página por separado.
    """
    if max_pages is None:
        max_pages = settings.pacientes_max_pages

    pacientes: List[Dict] = []
    visited = set()
    to_visit = [settings.pacientes_path]
    page_num = 0

    while to_visit and page_num < max_pages:
        path = to_visit.pop(0)
        if path in visited:
            continue
        visited.add(path)
        page_num += 1

        resp = client.get(path)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # Parseo simple de tabla; ajustar al markup real si cambia
        for row in soup.select("table tr"):
            cols = [c.get_text(strip=True) for c in row.find_all("td")]
            if cols:
                pacientes.append({"raw": cols})

        # Guardar HTML y assets sin borrar nada
        pipelines.save_html(f"pacientes_list_{page_num}", resp.text)
        pipelines.download_assets(resp.text, client)

        # Descubrir enlaces de paginación
        for a in soup.find_all("a"):
            href = a.get("href")
            if not href:
                continue
            abs_url = urljoin(client.base_url, href)
            if "pacientes" not in abs_url:
                continue
            rel = abs_url.replace(client.base_url, "/")
            if rel not in visited and rel not in to_visit and len(visited) + len(to_visit) < max_pages:
                to_visit.append(rel)

    pipelines.save_json("pacientes", pacientes)
    return pacientes
