#!/usr/bin/env python3
"""
Comparar 3 IDs de historias clínicas entre local (MySQL 3307) y legacy (MySQL 3308).
Legacy se obtiene vía Chromium autenticado (CDP 9222).
Local se obtiene vía HTTP en 127.0.0.1:8090.
"""
import argparse
import json
import random
import re
import subprocess
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


LEGACY_HC_URL = "https://cardioprietohc.com/index.php/hClinica/verHClinica/{id}"
LEGACY_HC_URL_ALT = "https://cardioprietohc.com/index.php/hClinica/ver/{id}"
LOCAL_HC_URL = "http://127.0.0.1:8090/historial_medico/{id}/"


FIELDS = [
    ("peso", "peso"),
    ("colesterol", "colesterol"),
    ("glucemia", "glucemia"),
    ("presionSistolica", "presion_sistolica"),
    ("presionDiastolica", "presion_diastolica"),
]


def _mysql_ids(port: int, table: str) -> set[str]:
    q = f"SELECT id FROM cardioprieto.{table};"
    out = subprocess.check_output(
        ["mysql", "-u", "root", "-P", str(port), "-pCorbis5", "-N", "-e", q]
    )
    return {line.decode().strip() for line in out.splitlines()}


def _mysql_ids_with_signs_local(port: int) -> set[str]:
    q = (
        "SELECT DISTINCT historia_id FROM cardioprieto.signos_vitales "
        "WHERE peso IS NOT NULL OR colesterol IS NOT NULL OR glucemia IS NOT NULL "
        "OR presion_sistolica IS NOT NULL OR presion_diastolica IS NOT NULL;"
    )
    out = subprocess.check_output(
        ["mysql", "-u", "root", "-P", str(port), "-pCorbis5", "-N", "-e", q]
    )
    return {line.decode().strip() for line in out.splitlines()}


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


def _is_login_page(html: str) -> bool:
    if not html:
        return True
    soup = BeautifulSoup(html, "html.parser")
    has_user = soup.find("input", {"name": "usuario"}) is not None
    has_pass = soup.find("input", {"name": "pass"}) is not None
    return has_user and has_pass


def _fetch_legacy_html(page, url: str) -> str:
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=10000)
        return page.content()
    except PlaywrightTimeoutError:
        return ""


def _extract_legacy_signs(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    values = {}
    for el in soup.find_all(["input", "select", "textarea"]):
        name = el.get("name")
        if not name:
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


def _extract_local_signs(html: str) -> dict:
    def find_js_value(key: str) -> str:
        patterns = [
            rf"{key}\\s*:\\s*'([^']*)'",
            rf'{key}\\s*:\\s*\"([^\"]*)\"',
            rf"{key}\\s*:\\s*([0-9.]+)",
        ]
        for pat in patterns:
            m = re.search(pat, html)
            if m:
                return m.group(1)
        return ""

    values = {}
    for legacy_key, local_key in FIELDS:
        values[local_key] = find_js_value(local_key)
    return values


def main():
    ap = argparse.ArgumentParser(description="Comparar 3 IDs de historias clínicas")
    ap.add_argument("--local-port", type=int, default=3307)
    ap.add_argument("--legacy-port", type=int, default=3308)
    ap.add_argument("--cdp-url", default="http://127.0.0.1:9222")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--out-dir", default="Scrap_cardioprietohc/data/reports")
    ap.add_argument("--exclude-ids", default="7544")
    args = ap.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    local_ids = _mysql_ids(args.local_port, "historias_clinicas")
    legacy_ids = _mysql_ids(args.legacy_port, "historiaclinica")
    inter = sorted(local_ids & legacy_ids)
    if not inter:
        raise SystemExit("No hay IDs en común entre local y legacy.")

    exclude_ids = {x.strip() for x in args.exclude_ids.split(",") if x.strip()}
    # prioriza IDs con signos vitales en local
    local_with_signs = _mysql_ids_with_signs_local(args.local_port)
    candidates = [i for i in inter if i in local_with_signs and i not in exclude_ids]
    if len(candidates) < 3:
        # completa con cualquier id en inter (excluyendo)
        candidates = [i for i in inter if i not in exclude_ids]
    ids = random.sample(candidates, k=min(3, len(candidates)))

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    report = {"ids": ids, "items": []}

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(args.cdp_url)
        context = _pick_authenticated_context(browser)

        for pid in ids:
            legacy_url = LEGACY_HC_URL.format(id=pid)
            local_url = LOCAL_HC_URL.format(id=pid)

            page = context.new_page()
            legacy_html = _fetch_legacy_html(page, legacy_url)
            if _is_login_page(legacy_html):
                legacy_html = _fetch_legacy_html(page, LEGACY_HC_URL_ALT.format(id=pid))
            page.close()

            if _is_login_page(legacy_html):
                report["items"].append(
                    {
                        "id": pid,
                        "legacy_url": legacy_url,
                        "local_url": local_url,
                        "status": "legacy_login_required",
                    }
                )
                continue

            legacy_vals = _extract_legacy_signs(legacy_html)

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

            local_vals = _extract_local_signs(local_resp.text)

            comparisons = []
            for legacy_key, local_key in FIELDS:
                lval = (legacy_vals.get(legacy_key, "") or "").strip()
                rval = (local_vals.get(local_key, "") or "").strip()
                comparisons.append(
                    {
                        "field": legacy_key,
                        "legacy_value": lval,
                        "local_value": rval,
                        "match": lval == rval,
                    }
                )

            report["items"].append(
                {
                    "id": pid,
                    "legacy_url": legacy_url,
                    "local_url": local_url,
                    "legacy_values": {k: legacy_vals.get(k, "") for k, _ in FIELDS},
                    "local_values": {k: local_vals.get(k, "") for _, k in FIELDS},
                    "comparisons": comparisons,
                    "status": "ok",
                }
            )

        browser.close()

    json_path = out_dir / "compare_legacy_local_histories_random_ids.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = ["# Comparación legacy vs local (3 IDs historias clínicas)", ""]
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

    md_path = out_dir / "compare_legacy_local_histories_random_ids.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
