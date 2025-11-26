from typing import List, Dict
from bs4 import BeautifulSoup

from ..client import ScrapClient
from .. import pipelines


def scrape_pacientes(client: ScrapClient) -> List[Dict]:
    # Ajustar path del endpoint real
    resp = client.get("/pacientes")
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    # TODO: parsear la tabla real
    pacientes = []
    for row in soup.select("table tr"):
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if not cols:
            continue
        pacientes.append({"raw": cols})

    pipelines.save_html("pacientes_list", resp.text)
    pipelines.save_json("pacientes", pacientes)
    return pacientes
