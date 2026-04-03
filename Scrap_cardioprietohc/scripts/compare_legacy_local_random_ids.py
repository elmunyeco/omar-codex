#!/usr/bin/env python3
"""
Comparar 3 IDs (aleatorios) entre legacy y local.
Legacy se obtiene vía Chromium autenticado (CDP 9222).
Local se obtiene vía HTTP en 127.0.0.1:8090.
"""
import argparse
import json
import random
import re
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


LEGACY_BASE = "https://cardioprietohc.com/index.php/pacientes/editar/"
LOCAL_BASE = "http://127.0.0.1:8090/pacientes/"


FIELDS = [
    "tipoDoc",
    "numDoc",
    "nombre",
    "apellido",
    "fechaNac",
    "sexo",
    "email",
    "direccion",
    "localidad",
    "obraSocial",
    "plan",
    "afiliado",
    "telefono",
    "celular",
    "profesion",
    "referente",
]


def _norm_date_ddmmyyyy(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", value)
    if m:
        y, mo, d = m.groups()
        return f"{d}/{mo}/{y}"
    m = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", value)
    if m:
        d, mo, y = m.groups()
        return f"{d}/{mo}/{y}"
    return value


def _norm_sexo_fm(value: str) -> str:
    v = (value or "").strip().lower()
    if v in ("f", "femenino", "mujer"):
        return "F"
    if v in ("m", "masculino", "h", "hombre"):
        return "M"
    return (value or "").strip()


def _norm_doctype(value: str) -> str:
    v = (value or "").strip()
    if not v:
        return ""
    # toma primer token alfabético (ej: "DNI (Documento...)" -> "DNI")
    m = re.match(r"^([A-Za-z]+)", v)
    return m.group(1).upper() if m else v.upper()


def _extract_values(html: str):
    soup = BeautifulSoup(html, "html.parser")
    values = {}
    for el in soup.find_all(["input", "select", "textarea"]):
        name = el.get("name")
        if not name or name == "csrfmiddlewaretoken":
            continue
        if el.name == "select":
            sel = el.find("option", selected=True)
            val = sel.get_text(strip=True) if sel else ""
        elif el.name == "textarea":
            val = el.get_text(strip=True)
        else:
            if el.get("type") in ("radio", "checkbox"):
                if not el.has_attr("checked"):
                    continue
                val = el.get("value", "")
            else:
                val = el.get("value", "")
        values[name] = val
    return values


def _fetch_legacy_html(page, url: str) -> str:
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=10000)
        return page.content()
    except PlaywrightTimeoutError:
        return ""


def _is_login_page(html: str) -> bool:
    if not html:
        return True
    soup = BeautifulSoup(html, "html.parser")
    has_user = soup.find("input", {"name": "usuario"}) is not None
    has_pass = soup.find("input", {"name": "pass"}) is not None
    return has_user and has_pass


def _pick_random_ids(list_pages):
    ids = set()
    for path in list_pages:
        text = Path(path).read_text(encoding="utf-8", errors="ignore")
        # extrae ids de links /pacientes/editar/<id>
        ids.update(re.findall(r"/pacientes/editar/(\d+)", text))
    ids = sorted(ids)
    if not ids:
        return []
    k = min(3, len(ids))
    return random.sample(ids, k=k)


def _pick_random_ids_from_intersection(legacy_pages, local_pages):
    legacy_ids = set()
    for path in legacy_pages:
        text = Path(path).read_text(encoding="utf-8", errors="ignore")
        legacy_ids.update(re.findall(r"/pacientes/editar/(\d+)", text))

    local_ids = set()
    for path in local_pages:
        text = Path(path).read_text(encoding="utf-8", errors="ignore")
        local_ids.update(re.findall(r"/pacientes/(\d+)/editar/", text))

    ids = sorted(legacy_ids & local_ids)
    if not ids:
        return []
    k = min(3, len(ids))
    return random.sample(ids, k=k)


def _pick_authenticated_context(browser):
    for ctx in browser.contexts:
        try:
            cookies = ctx.cookies("https://cardioprietohc.com")
        except Exception:
            cookies = []
        if cookies:
            return ctx
        for page in ctx.pages:
            if "cardioprietohc.com" in (page.url or ""):
                return ctx
    return browser.contexts[0] if browser.contexts else browser.new_context()


def main():
    ap = argparse.ArgumentParser(description="Comparar 3 IDs legacy vs local")
    ap.add_argument(
        "--legacy-list-pages",
        nargs="+",
        default=[
            "scrap_legacy/crawl_7544/site_mirror/index-php-pacientes-listar-1.html",
            "scrap_legacy/crawl_7544/site_mirror/index-php-pacientes-listar-2.html",
        ],
    )
    ap.add_argument(
        "--local-list-pages",
        nargs="+",
        default=[
            "Scrap_cardioprietohc/data/raw/local_crawl_8090_2026-03-24/pacientes_list_1.html",
            "Scrap_cardioprietohc/data/raw/local_crawl_8090_2026-03-24/pacientes_list_2.html",
            "Scrap_cardioprietohc/data/raw/local_crawl_8090_2026-03-24/pacientes_list_3.html",
            "Scrap_cardioprietohc/data/raw/local_crawl_8090_2026-03-24/pacientes_list_4.html",
            "Scrap_cardioprietohc/data/raw/local_crawl_8090_2026-03-24/pacientes_list_5.html",
            "Scrap_cardioprietohc/data/raw/local_crawl_8090_2026-03-24/pacientes_list_6.html",
            "Scrap_cardioprietohc/data/raw/local_crawl_8090_2026-03-24/pacientes_list_7.html",
            "Scrap_cardioprietohc/data/raw/local_crawl_8090_2026-03-24/pacientes_list_8.html",
            "Scrap_cardioprietohc/data/raw/local_crawl_8090_2026-03-24/pacientes_list_9.html",
            "Scrap_cardioprietohc/data/raw/local_crawl_8090_2026-03-24/pacientes_list_10.html",
            "Scrap_cardioprietohc/data/raw/local_crawl_8090_2026-03-24/pacientes_list_11.html",
            "Scrap_cardioprietohc/data/raw/local_crawl_8090_2026-03-24/pacientes_list_12.html",
            "Scrap_cardioprietohc/data/raw/local_crawl_8090_2026-03-24/pacientes_list_13.html",
            "Scrap_cardioprietohc/data/raw/local_crawl_8090_2026-03-24/pacientes_list_14.html",
        ],
    )
    ap.add_argument("--cdp-url", default="http://127.0.0.1:9222")
    ap.add_argument("--out-dir", default="Scrap_cardioprietohc/data/reports")
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    ids = _pick_random_ids_from_intersection(args.legacy_list_pages, args.local_list_pages)
    selection_strategy = "intersection"
    if not ids:
        # fallback: usa legacy aunque no estén en local
        ids = _pick_random_ids(args.legacy_list_pages)
        if not ids:
            raise SystemExit("No se encontraron IDs en las páginas legacy.")
        selection_strategy = "legacy_fallback_no_overlap"

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "ids": ids,
        "selection_strategy": selection_strategy,
        "items": [],
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(args.cdp_url)
        context = _pick_authenticated_context(browser)

        for pid in ids:
            legacy_url = f"{LEGACY_BASE}{pid}"
            local_url = f"{LOCAL_BASE}{pid}/editar/"

            page = context.new_page()
            legacy_html = _fetch_legacy_html(page, legacy_url)
            page.close()

            if _is_login_page(legacy_html):
                status = "legacy_login_required"
                report["items"].append(
                    {"id": pid, "legacy_url": legacy_url, "local_url": local_url, "status": status}
                )
                continue

            legacy_vals = _extract_values(legacy_html)

            local_resp = httpx.get(local_url)
            if not local_resp.is_success:
                report["items"].append(
                    {
                        "id": pid,
                        "legacy_url": legacy_url,
                        "local_url": local_url,
                        "status": "local_missing",
                    }
                )
                continue
            local_vals = _extract_values(local_resp.text)

            # normalizaciones por campo
            def norm_field(name, value):
                if name == "fechaNac":
                    return _norm_date_ddmmyyyy(value)
                if name == "sexo":
                    return _norm_sexo_fm(value)
                if name == "tipoDoc":
                    return _norm_doctype(value)
                return (value or "").strip()

            comparisons = []
            for field in FIELDS:
                legacy_key = field
                local_key = field
                if field == "tipoDoc":
                    local_key = "idTipoDoc"
                if field == "email":
                    local_key = "mail"

                legacy_val = legacy_vals.get(legacy_key, "")
                local_val = local_vals.get(local_key, "")

                legacy_val_n = norm_field(field, legacy_val)
                local_val_n = norm_field(field, local_val)

                comparisons.append(
                    {
                        "field": field,
                        "legacy_value": legacy_val_n,
                        "local_value": local_val_n,
                        "match": legacy_val_n == local_val_n,
                    }
                )

            report["items"].append(
                {
                    "id": pid,
                    "legacy_url": legacy_url,
                    "local_url": local_url,
                    "legacy_values": legacy_vals,
                    "local_values": local_vals,
                    "comparisons": comparisons,
                    "status": "ok",
                }
            )

        browser.close()

    json_path = out_dir / "compare_legacy_local_random_ids.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = ["# Comparación legacy vs local (3 IDs aleatorios)", ""]
    md_lines.append(f"- IDs: {', '.join(ids)}")
    md_lines.append("")
    for item in report["items"]:
        md_lines.append(f"## ID {item['id']}")
        md_lines.append(f"- Legacy: `{item.get('legacy_url','')}`")
        md_lines.append(f"- Local: `{item.get('local_url','')}`")
        md_lines.append(f"- Status: {item.get('status','')}")
        if item.get("status") != "ok":
            md_lines.append("")
            continue
        md_lines.append("### Comparación")
        for c in item["comparisons"]:
            mark = "OK" if c["match"] else "DIFF"
            md_lines.append(
                f"- {c['field']}: legacy='{c['legacy_value']}' | local='{c['local_value']}' => {mark}"
            )
        md_lines.append("")

    md_path = out_dir / "compare_legacy_local_random_ids.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
