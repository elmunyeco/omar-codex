#!/usr/bin/env python3
"""
Prueba de idempotencia vía UI (legacy y local) usando el ID 7544.
No usa DB. Interactúa con la UI y mide cambios visibles.
"""
import json
import os
import time
from pathlib import Path

import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

LEGACY_URL = os.getenv(
    "LEGACY_URL", "https://cardioprietohc.com/index.php/hClinica/verHClinica/7544"
)
LEGACY_URL_ALT = os.getenv(
    "LEGACY_URL_ALT", "https://cardioprietohc.com/index.php/hClinica/ver/7544"
)
LOCAL_URL = os.getenv("LOCAL_URL", "http://127.0.0.1:8090/historial_medico/7544/")
LOCAL_USER = os.getenv("LOCAL_USER", "omar")
LOCAL_PASS = os.getenv("LOCAL_PASS", "Corbis5")

COMMENT_TOKEN = f"TEST_IDEMPOTENCIA_{int(time.time())}"
SIGNS = {
    "peso": "71.11",
    "colesterol": "180",
    "glucemia": "90",
    "presionSistolica": "120",
    "presionDiastolica": "80",
}
LOCAL_SIGNS = {
    "estado.signos_vitales.peso": "71.11",
    "estado.signos_vitales.colesterol": "180",
    "estado.signos_vitales.glucemia": "90",
    "estado.signos_vitales.presion_sistolica": "120",
    "estado.signos_vitales.presion_diastolica": "80",
}


def count_legacy_comments(html: str) -> int:
    return html.count("hClinica/eliminarComentario/")


def count_legacy_signs_value(html: str, value: str) -> int:
    return html.count(value)


def is_login(html: str) -> bool:
    return "name=\"usuario\"" in html and "name=\"pass\"" in html


def pick_authenticated_context(browser):
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


def legacy_fetch(page, url):
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=10000)
        return page.content()
    except PlaywrightTimeoutError:
        return ""


def ensure_legacy_hc_page(page) -> str:
    html = legacy_fetch(page, LEGACY_URL)
    if is_login(html):
        html = legacy_fetch(page, LEGACY_URL_ALT)
    # if comment form not found, try alternate URL once more
    if page.locator("form[action*='nuevoComentario']").count() == 0:
        html = legacy_fetch(page, LEGACY_URL_ALT)
    return html


def legacy_reload_hc(page) -> str:
    html = legacy_fetch(page, LEGACY_URL)
    if is_login(html):
        html = legacy_fetch(page, LEGACY_URL_ALT)
    return html


def legacy_submit_comment(page, comment: str):
    # wait until form appears (custom loop to avoid visibility issues)
    for _ in range(50):
        if page.locator("form[action*='nuevoComentario'] textarea[name='comentario']").count() > 0:
            break
        page.wait_for_timeout(200)
    if page.locator("form[action*='nuevoComentario'] textarea[name='comentario']").count() == 0:
        page.reload(wait_until="domcontentloaded")
    if page.locator("form[action*='nuevoComentario'] textarea[name='comentario']").count() == 0:
        # dump for debugging
        html = page.content()
        Path("Scrap_cardioprietohc/data/reports/legacy_hc_7544_dump.html").write_text(html, encoding="utf-8")
        raise RuntimeError("No se encontró el formulario de comentario en legacy. Dump guardado en data/reports/legacy_hc_7544_dump.html")
    page.eval_on_selector(
        "form[action*='nuevoComentario'] textarea[name='comentario']",
        "(el, value) => { el.value = value; }",
        comment,
    )
    page.evaluate("document.querySelector(\"form[action*='nuevoComentario']\").submit()")
    # response may be a bare '1'; reload HC
    page.wait_for_timeout(500)
    legacy_reload_hc(page)


def legacy_submit_signs(page, signs: dict):
    for _ in range(50):
        if page.locator("form[action*='nuevoSignoVital']").count() > 0:
            break
        page.wait_for_timeout(200)
    if page.locator("form[action*='nuevoSignoVital']").count() == 0:
        page.reload(wait_until="domcontentloaded")
    if page.locator("form[action*='nuevoSignoVital']").count() == 0:
        raise RuntimeError("No se encontró el formulario de signos vitales en legacy.")
    for name, val in signs.items():
        page.eval_on_selector(
            f"input[name='{name}']",
            "(el, value) => { el.value = value; }",
            val,
        )
    page.evaluate("document.querySelector(\"form[action*='nuevoSignoVital']\").submit()")
    page.wait_for_timeout(500)
    legacy_reload_hc(page)


def local_get_visits_count(page) -> int:
    # count rendered visit panels
    return page.locator("div[x-data='historialMedico'] div.border.rounded-lg").count()


def local_get_comment_value(page) -> str:
    return page.locator("textarea[x-model='estado.comentarios']").input_value()


def local_set_signs_and_comment(page, comment: str, signs: dict):
    for model, val in signs.items():
        locator = page.locator(f"[x-model='{model}']")
        locator.fill(val)
        locator.dispatch_event("input")
    comment_area = page.locator("textarea[x-model='estado.comentarios']")
    comment_area.fill(comment)
    comment_area.dispatch_event("input")
    page.wait_for_timeout(200)


def local_click_save(page):
    # button with @click or x-on:click
    btn = page.locator("button:has-text('Guardar')")
    if btn.count() == 0:
        btn = page.locator("[x-on\\:click='guardarCambios()'], [\\@click='guardarCambios()']")
    try:
        with page.expect_navigation(timeout=7000):
            btn.first.click()
    except Exception:
        btn.first.click()
    page.wait_for_load_state("domcontentloaded")


def local_login_if_needed(page):
    login_url = os.getenv("LOCAL_LOGIN_URL", "http://127.0.0.1:8080/login/")
    page.goto(login_url, wait_until="domcontentloaded", timeout=10000)
    if page.locator("input[name='username']").count() == 0:
        return
    page.fill("input[name='username']", LOCAL_USER)
    page.fill("input[name='password']", LOCAL_PASS)
    btn = page.locator("button[type='submit'], button:has-text('Ingresar')")
    if btn.count() == 0:
        btn = page.locator("input[type='submit']")
    if btn.count() == 0:
        return
    try:
        with page.expect_navigation(timeout=10000):
            btn.first.click()
    except Exception:
        btn.first.click()
    page.wait_for_load_state("domcontentloaded")


def main():
    report = {
        "comment_token": COMMENT_TOKEN,
        "legacy": {},
        "local": {},
    }

    with sync_playwright() as p:
        # LEGACY via CDP
        cdp_url = os.getenv("CDP_URL", "http://127.0.0.1:9222")
        browser = p.chromium.connect_over_cdp(cdp_url)
        context = pick_authenticated_context(browser)
        page = context.new_page()

        html = ensure_legacy_hc_page(page)
        if is_login(html):
            raise RuntimeError("Legacy no autenticado en CDP (login requerido).")
        before_comments = count_legacy_comments(html)

        # submit comment twice
        legacy_submit_comment(page, COMMENT_TOKEN)
        html1 = page.content()
        after_comments_1 = count_legacy_comments(html1)

        legacy_submit_comment(page, COMMENT_TOKEN)
        html2 = page.content()
        after_comments_2 = count_legacy_comments(html2)

        # signs: count occurrences of peso value in HTML
        html3 = page.content()
        before_signs_count = count_legacy_signs_value(html3, SIGNS["peso"])

        legacy_submit_signs(page, SIGNS)
        html4 = page.content()
        after_signs_1 = count_legacy_signs_value(html4, SIGNS["peso"])

        legacy_submit_signs(page, SIGNS)
        html5 = page.content()
        after_signs_2 = count_legacy_signs_value(html5, SIGNS["peso"])

        report["legacy"] = {
            "comments_count": [before_comments, after_comments_1, after_comments_2],
            "signs_peso_occurrences": [before_signs_count, after_signs_1, after_signs_2],
        }

        page.close()
        browser.close()

        # LOCAL via UI (headless)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        local_login_if_needed(page)
        page.goto(LOCAL_URL, wait_until="domcontentloaded")

        before_visits = local_get_visits_count(page)
        before_comment = local_get_comment_value(page)

        local_set_signs_and_comment(page, COMMENT_TOKEN, LOCAL_SIGNS)
        with page.expect_response("**/api/historia/7544/guardar/", timeout=7000) as resp1:
            local_click_save(page)
        resp1_status = resp1.value.status

        after_visits_1 = local_get_visits_count(page)
        after_comment_1 = local_get_comment_value(page)

        local_set_signs_and_comment(page, COMMENT_TOKEN, LOCAL_SIGNS)
        with page.expect_response("**/api/historia/7544/guardar/", timeout=7000) as resp2:
            local_click_save(page)
        resp2_status = resp2.value.status

        after_visits_2 = local_get_visits_count(page)
        after_comment_2 = local_get_comment_value(page)

        report["local"] = {
            "visits_count": [before_visits, after_visits_1, after_visits_2],
            "comment_value": [before_comment, after_comment_1, after_comment_2],
            "save_status": [resp1_status, resp2_status],
        }

        page.close()
        browser.close()

    out_json = Path("Scrap_cardioprietohc/data/reports/idempotency_ui_7544.json")
    out_md = Path("Scrap_cardioprietohc/data/reports/idempotency_ui_7544.md")
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md = []
    md.append("# Idempotencia UI (ID 7544)")
    md.append("")
    md.append(f"- Token comentario: `{COMMENT_TOKEN}`")
    md.append("")
    md.append("## Legacy")
    md.append(f"- comentarios_count (before, after1, after2): {report['legacy']['comments_count']}")
    md.append(f"- signs_peso_occurrences (before, after1, after2): {report['legacy']['signs_peso_occurrences']}")
    md.append("")
    md.append("## Local")
    md.append(f"- visitas_count (before, after1, after2): {report['local']['visits_count']}")
    md.append(f"- comentario (before, after1, after2): {report['local']['comment_value']}")
    md.append(f"- save_status (after1, after2): {report['local']['save_status']}")

    out_md.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
