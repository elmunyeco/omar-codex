#!/usr/bin/env python3
"""
Matriz funcional legacy vs local.
Usa CDP 9222 para legacy y HTTP local para 127.0.0.1:8090.
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

LEGACY_BASE = "https://cardioprietohc.com/index.php"
LOCAL_BASE = "http://127.0.0.1:8090"


def _mysql_fetch_pairs(port: int):
    q = (
        "SELECT hc.id AS historia_id, hc.paciente_id AS paciente_id "
        "FROM cardioprieto.historias_clinicas hc;"
    )
    out = subprocess.check_output(["mysql", "-u", "root", "-P", str(port), "-pCorbis5", "-N", "-e", q])
    pairs = []
    for line in out.splitlines():
        parts = line.decode().strip().split("\t")
        if len(parts) == 2:
            pairs.append((parts[0], parts[1]))
    return pairs


def _mysql_fetch_pairs_legacy(port: int):
    q = (
        "SELECT hc.id AS historia_id, hc.idPaciente AS paciente_id "
        "FROM cardioprieto.historiaclinica hc;"
    )
    out = subprocess.check_output(["mysql", "-u", "root", "-P", str(port), "-pCorbis5", "-N", "-e", q])
    pairs = []
    for line in out.splitlines():
        parts = line.decode().strip().split("\t")
        if len(parts) == 2:
            pairs.append((parts[0], parts[1]))
    return pairs


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


def _legacy_checks(html: str) -> dict:
    return {
        "has_pacientes_list_link": "pacientes/index" in html,
        "has_hclinica_list_link": "hClinica/index" in html,
        "has_descargar_hc": "hClinica/descargarHClinica" in html,
        "has_estudios_listar": "estudios/listarEstudios" in html,
        "has_form_diagnosticos": "hClinica/editarDiagnostico" in html,
        "has_form_comentario": "hClinica/nuevoComentario" in html,
        "has_form_signos": "hClinica/nuevoSignoVital" in html,
        "has_form_indicaciones": "hClinica/enviarIndicaciones" in html,
        "comentarios_count": len(re.findall(r"hClinica/eliminarComentario/\d+", html)),
    }


def _legacy_list_checks(html: str) -> dict:
    return {
        "has_pagination": "page" in html and "pagination" in html.lower(),
        "has_edit_links": bool(re.search(r"/pacientes/editar/\d+", html)),
    }


def _legacy_hc_list_checks(html: str) -> dict:
    return {
        "has_ver_hc_links": bool(re.search(r"/hClinica/verHClinica/\d+", html)),
    }


def _local_checks(html: str) -> dict:
    return {
        "has_condiciones_key": "condiciones" in html,
        "has_comentarios_key": "comentarios" in html,
        "has_signos_vitales_key": "signos_vitales" in html,
        "has_indicaciones_key": "indicaciones" in html,
    }


def _local_list_checks(html: str) -> dict:
    return {
        "has_pagination": "page=" in html,
        "has_edit_links": bool(re.search(r"/pacientes/\d+/editar/", html)),
    }


def _local_hc_list_checks(html: str) -> dict:
    return {
        "has_historial_links": bool(re.search(r"/historial_medico/\d+/", html)),
    }


def main():
    ap = argparse.ArgumentParser(description="Matriz funcional legacy vs local")
    ap.add_argument("--local-port", type=int, default=3307)
    ap.add_argument("--legacy-port", type=int, default=3308)
    ap.add_argument("--cdp-url", default="http://127.0.0.1:9222")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--exclude-ids", default="7544")
    ap.add_argument("--out-dir", default="Scrap_cardioprietohc/data/reports")
    args = ap.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    local_pairs = _mysql_fetch_pairs(args.local_port)
    legacy_pairs = _mysql_fetch_pairs_legacy(args.legacy_port)
    legacy_by_hist = {h: p for h, p in legacy_pairs}

    exclude = {x.strip() for x in args.exclude_ids.split(",") if x.strip()}
    inter = [(h, p) for h, p in local_pairs if h in legacy_by_hist and h not in exclude]
    if not inter:
        raise SystemExit("No hay historias en común (excluyendo).")

    sample = random.sample(inter, k=min(3, len(inter)))

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "sample": [{"historia_id": h, "paciente_id": p} for h, p in sample],
        "items": [],
    }

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(args.cdp_url)
        context = _pick_authenticated_context(browser)

        # Legacy list pages
        page = context.new_page()
        legacy_pac_list = _fetch_legacy_html(page, f"{LEGACY_BASE}/pacientes/index")
        legacy_hc_list = _fetch_legacy_html(page, f"{LEGACY_BASE}/hClinica/index")
        page.close()

        report["legacy_list_checks"] = {
            "pacientes": _legacy_list_checks(legacy_pac_list) if not _is_login_page(legacy_pac_list) else {"error": "login"},
            "historias": _legacy_hc_list_checks(legacy_hc_list) if not _is_login_page(legacy_hc_list) else {"error": "login"},
        }

        browser.close()

    # Local list pages
    local_pac_list = httpx.get(f"{LOCAL_BASE}/pacientes/").text
    local_hc_list = httpx.get(f"{LOCAL_BASE}/historias/").text
    report["local_list_checks"] = {
        "pacientes": _local_list_checks(local_pac_list),
        "historias": _local_hc_list_checks(local_hc_list),
    }

    # Per-sample pages
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(args.cdp_url)
        context = _pick_authenticated_context(browser)

        for historia_id, paciente_id in sample:
            legacy_hc_url = f"{LEGACY_BASE}/hClinica/verHClinica/{historia_id}"
            legacy_hc_url_alt = f"{LEGACY_BASE}/hClinica/ver/{historia_id}"
            legacy_pac_url = f"{LEGACY_BASE}/pacientes/editar/{paciente_id}"

            page = context.new_page()
            legacy_hc_html = _fetch_legacy_html(page, legacy_hc_url)
            if _is_login_page(legacy_hc_html):
                legacy_hc_html = _fetch_legacy_html(page, legacy_hc_url_alt)
            legacy_pac_html = _fetch_legacy_html(page, legacy_pac_url)
            page.close()

            legacy_ok = not _is_login_page(legacy_hc_html)
            legacy_pac_ok = not _is_login_page(legacy_pac_html)

            local_hc_url = f"{LOCAL_BASE}/historial_medico/{historia_id}/"
            local_pac_url = f"{LOCAL_BASE}/pacientes/{paciente_id}/editar/"

            local_hc_resp = httpx.get(local_hc_url)
            local_pac_resp = httpx.get(local_pac_url)

            item = {
                "historia_id": historia_id,
                "paciente_id": paciente_id,
                "legacy": {
                    "hc_url": legacy_hc_url,
                    "pac_url": legacy_pac_url,
                    "hc_ok": legacy_ok,
                    "pac_ok": legacy_pac_ok,
                    "hc_checks": _legacy_checks(legacy_hc_html) if legacy_ok else {"error": "login"},
                },
                "local": {
                    "hc_url": local_hc_url,
                    "pac_url": local_pac_url,
                    "hc_ok": local_hc_resp.is_success,
                    "pac_ok": local_pac_resp.is_success,
                    "hc_checks": _local_checks(local_hc_resp.text) if local_hc_resp.is_success else {"error": "http"},
                },
            }
            report["items"].append(item)

        browser.close()

    json_path = out_dir / "functional_matrix_report.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md = []
    md.append("# Matriz funcional legacy vs local")
    md.append("")
    md.append("## Listas")
    md.append(f"- legacy.pacientes: {report['legacy_list_checks']['pacientes']}")
    md.append(f"- legacy.historias: {report['legacy_list_checks']['historias']}")
    md.append(f"- local.pacientes: {report['local_list_checks']['pacientes']}")
    md.append(f"- local.historias: {report['local_list_checks']['historias']}")
    md.append("")

    md.append("## Muestras")
    for it in report["items"]:
        md.append(f"### HC {it['historia_id']} / Paciente {it['paciente_id']}")
        md.append(f"- legacy.hc_url: `{it['legacy']['hc_url']}`")
        md.append(f"- legacy.pac_url: `{it['legacy']['pac_url']}`")
        md.append(f"- legacy.hc_checks: {it['legacy']['hc_checks']}")
        md.append(f"- local.hc_url: `{it['local']['hc_url']}`")
        md.append(f"- local.pac_url: `{it['local']['pac_url']}`")
        md.append(f"- local.hc_checks: {it['local']['hc_checks']}")
        md.append("")

    md_path = out_dir / "functional_matrix_report.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
