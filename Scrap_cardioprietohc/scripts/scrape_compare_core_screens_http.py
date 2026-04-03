#!/usr/bin/env python3
"""
Scrapea pantallas core (legacy + local) usando login HTTP (no CDP),
captura HTML + JPG, y genera reporte MD/JSON.
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
from datetime import date
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MD_PATH = Path("Scrap_cardioprietohc/data/reports/pantallas_core_map_2026-03-24.md")
OUT_BASE = Path("Scrap_cardioprietohc/data/raw") / f"core_screens_{date.today().isoformat()}"
LEGACY_BASE = "https://cardioprietohc.com"
LOCAL_BASE = "http://127.0.0.1:8090"
LOGIN_URL = f"{LEGACY_BASE}/index.php/login/validarUsuario"

LEGACY_USER = os.getenv("LEGACY_USER", "")
LEGACY_PASS = os.getenv("LEGACY_PASS", "")


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_").lower()
    return s or "item"


def parse_sections(md_text: str):
    sections = []
    pattern = re.compile(r"^###\s+(.+)$", re.M)
    heads = list(pattern.finditer(md_text))
    for i, h in enumerate(heads):
        start = h.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(md_text)
        block = md_text[start:end]
        title = h.group(1).strip()

        def get_line(prefix: str):
            m = re.search(rf"^-\s*{re.escape(prefix)}:\s*(.+)$", block, re.M)
            return m.group(1).strip() if m else None

        legacy = get_line("Legacy")
        local = get_line("Local")
        sections.append({"title": title, "legacy": legacy, "local": local})
    return sections


def resolve(url: str | None, base: str) -> str | None:
    if not url or url.startswith("("):
        return None
    url = url.strip()
    if url.lower().startswith("embebido"):
        return None
    m = re.search(r"`([^`]+)`", url)
    if m:
        url = m.group(1)
    if "descargarHClinica" in url:
        return None
    if url.startswith("http://") or url.startswith("https://"):
        return url
    url = url.replace("{id}", "7544").replace("{paciente_id}", "7544").replace("{n}", "1")
    return base.rstrip("/") + url


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)


def is_login_page(html: str) -> bool:
    soup = BeautifulSoup(html, "html.parser")
    return soup.find("input", {"name": "usuario"}) is not None and soup.find(
        "input", {"name": "pass"}
    ) is not None


def main() -> int:
    if not (LEGACY_USER and LEGACY_PASS):
        print("LEGACY_USER/LEGACY_PASS faltan")
        return 1

    md_text = MD_PATH.read_text(encoding="utf-8")
    sections = parse_sections(md_text)

    legacy_dir = OUT_BASE / "legacy"
    local_dir = OUT_BASE / "local"
    legacy_shots = OUT_BASE / "legacy_shots"
    local_shots = OUT_BASE / "local_shots"
    for p in (legacy_dir, local_dir, legacy_shots, local_shots):
        p.mkdir(parents=True, exist_ok=True)

    # Login legacy via HTTP
    client = httpx.Client(follow_redirects=True)
    client.get(f"{LEGACY_BASE}/index.php/")
    client.post(LOGIN_URL, data={"usuario": LEGACY_USER, "pass": LEGACY_PASS})
    # Debug: verify login
    try:
        test_html = client.get(f"{LEGACY_BASE}/index.php/pacientes/index").text
        Path("Scrap_cardioprietohc/data/reports/compare_core_screens_logincheck.txt").write_text(
            f"logincheck_pacientes={'login' if is_login_page(test_html) else 'ok'}\\n",
            encoding="utf-8",
        )
    except Exception as e:
        Path("Scrap_cardioprietohc/data/reports/compare_core_screens_logincheck.txt").write_text(
            f"logincheck_error={e}\\n",
            encoding="utf-8",
        )

    results = []

    with sync_playwright() as p:
        legacy_browser = p.chromium.launch(headless=True)
        legacy_page = legacy_browser.new_page()
        local_browser = p.chromium.launch(headless=True)
        local_page = local_browser.new_page()

        for s in sections:
            title = s["title"]
            slug = slugify(title)
            legacy_url = resolve(s.get("legacy"), LEGACY_BASE)
            local_url = resolve(s.get("local"), LOCAL_BASE)

            item = {
                "title": title,
                "slug": slug,
                "legacy_url": legacy_url,
                "local_url": local_url,
                "legacy_html": None,
                "local_html": None,
                "legacy_shot": None,
                "local_shot": None,
                "legacy_error": None,
                "local_error": None,
            }

            if legacy_url:
                try:
                    resp = client.get(legacy_url, timeout=15.0)
                    html = resp.text
                    if is_login_page(html):
                        item["legacy_error"] = "login_required"
                        results.append(item)
                        continue
                    html_path = legacy_dir / f"{slug}.html"
                    html_path.write_text(html, encoding="utf-8")
                    shot_path = legacy_shots / f"{slug}.jpg"
                    legacy_page.set_viewport_size({"width": 1400, "height": 900})
                    legacy_page.set_content(html, wait_until="domcontentloaded")
                    legacy_page.wait_for_timeout(200)
                    legacy_page.screenshot(path=str(shot_path), type="jpeg", quality=80, full_page=True)
                    item["legacy_html"] = str(html_path)
                    item["legacy_shot"] = str(shot_path)
                except Exception as e:
                    item["legacy_error"] = str(e)

            if local_url:
                try:
                    local_page.set_viewport_size({"width": 1400, "height": 900})
                    local_page.goto(local_url, wait_until="domcontentloaded", timeout=10000)
                    local_page.wait_for_timeout(1200)
                    html = local_page.content()
                    html_path = local_dir / f"{slug}.html"
                    html_path.write_text(html, encoding="utf-8")
                    shot_path = local_shots / f"{slug}.jpg"
                    local_page.screenshot(path=str(shot_path), type="jpeg", quality=80, full_page=True)
                    item["local_html"] = str(html_path)
                    item["local_shot"] = str(shot_path)
                except Exception as e:
                    item["local_error"] = str(e)

            results.append(item)

        legacy_browser.close()
        local_browser.close()

    # Semantic comparison
    docs = []
    doc_keys = []
    for item in results:
        for side in ("legacy", "local"):
            html_path = item.get(f"{side}_html")
            if not html_path:
                continue
            html = Path(html_path).read_text(encoding="utf-8", errors="ignore")
            text = html_to_text(html)
            docs.append(text)
            doc_keys.append((item["slug"], side))

    sim_map = {}
    if docs:
        vec = TfidfVectorizer(max_features=5000)
        mat = vec.fit_transform(docs)
        for item in results:
            slug = item["slug"]
            try:
                i = doc_keys.index((slug, "legacy"))
                j = doc_keys.index((slug, "local"))
            except ValueError:
                continue
            score = float(cosine_similarity(mat[i], mat[j])[0][0])
            sim_map[slug] = score

    report_path = Path("Scrap_cardioprietohc/data/reports/compare_core_screens_2026-03-25.md")
    lines = [
        "# Comparación Semántica de Pantallas Core (Legacy vs Local)",
        "",
        "Fecha: 2026-03-25",
        "",
        "## Alcance",
        f"- Legacy: {LEGACY_BASE} (login HTTP)",
        f"- Local: {LOCAL_BASE}",
        "- Fuentes: HTML y capturas JPG generadas en data/raw",
        "- Estudios excluidos",
        "",
    ]

    for item in results:
        title = item["title"]
        slug = item["slug"]
        lines.append(f"## {title}")
        lines.append("")
        lines.append(f"- Legacy URL: {item['legacy_url'] or '(sin equivalente)'}")
        lines.append(f"- Local URL: {item['local_url'] or '(sin equivalente)'}")
        lines.append(f"- Similaridad TF-IDF: {sim_map.get(slug, 'N/A')}")
        if item.get("legacy_error"):
            lines.append(f"- Legacy error: {item['legacy_error']}")
        if item.get("local_error"):
            lines.append(f"- Local error: {item['local_error']}")
        lines.append("")
        if item.get("legacy_shot"):
            lines.append(f"![Legacy - {title}]({Path(item['legacy_shot']).as_posix()})")
        else:
            lines.append("Legacy: sin captura.")
        if item.get("local_shot"):
            lines.append(f"![Local - {title}]({Path(item['local_shot']).as_posix()})")
        else:
            lines.append("Local: sin captura.")
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    json_path = Path("Scrap_cardioprietohc/data/reports/compare_core_screens_2026-03-25.json")
    json_path.write_text(json.dumps({"results": results, "similarity": sim_map}, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
