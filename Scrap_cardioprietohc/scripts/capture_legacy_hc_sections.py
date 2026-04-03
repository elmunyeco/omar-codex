#!/usr/bin/env python3
"""
Captura secciones embebidas dentro de la Historia Clínica legacy (7544)
para tener "sub‑pantallas" rasterizadas.
"""
from __future__ import annotations

import os
from pathlib import Path

from playwright.sync_api import sync_playwright

LEGACY_BASE = "https://cardioprietohc.com"
HC_URL = f"{LEGACY_BASE}/index.php/hClinica/verHClinica/7544"
USER = os.getenv("LEGACY_USER", "")
PASS = os.getenv("LEGACY_PASS", "")
OUT_DIR = Path("Scrap_cardioprietohc/data/raw/core_screens_2026-03-25/legacy_hc_sections")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SECTIONS = [
    "Signos Vitales",
    "Condiciones Médicas",
    "Historial de Visitas Médicas",
    "Indicaciones",
]


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()
        page.goto(f"{LEGACY_BASE}/index.php/", wait_until="domcontentloaded", timeout=10000)
        if page.locator("input[name='usuario']").count() > 0:
            page.fill("input[name='usuario']", USER)
            page.fill("input[name='pass']", PASS)
            if page.locator("button[type='submit']").count() > 0:
                page.click("button[type='submit']")
            else:
                page.locator("input[type='submit']").first.click()
            page.wait_for_timeout(1500)

        page.goto(HC_URL, wait_until="domcontentloaded", timeout=10000)
        page.wait_for_timeout(1200)

        # expand all collapses if any
        try:
            page.eval_on_selector_all("[data-toggle='collapse']", "els => els.forEach(e => e.click())")
        except Exception:
            pass

        page.set_viewport_size({"width": 1400, "height": 900})

        for name in SECTIONS:
            # find element containing section title
            locator = page.locator(f"xpath=//*[contains(normalize-space(.), '{name}')]").first
            if locator.count() == 0:
                continue
            # try to capture nearest container
            handle = locator.evaluate_handle(
                """
                (el) => el.closest('.panel, .card, .box, section, .row, .col, .container, div') || el
                """
            )
            try:
                handle.screenshot(path=str(OUT_DIR / f"legacy_hc_{name.replace(' ', '_').lower()}.jpg"), type="jpeg", quality=80)
            except Exception:
                # fallback full-page
                page.screenshot(path=str(OUT_DIR / f"legacy_hc_{name.replace(' ', '_').lower()}.jpg"), type="jpeg", quality=80, full_page=True)

        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
