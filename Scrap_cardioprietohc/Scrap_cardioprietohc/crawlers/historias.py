from typing import List, Dict
from bs4 import BeautifulSoup

from ..client import ScrapClient
from .. import pipelines


def scrape_historias(client: ScrapClient) -> List[Dict]:
    # Ajustar path del endpoint real
    resp = client.get("/historias")
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    historias = []
    for row in soup.select("table tr"):
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if not cols:
            continue
        historias.append({"raw": cols})

    pipelines.save_html("historias_list", resp.text)
    pipelines.save_json("historias", historias)
    return historias
