import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from playwright.async_api import async_playwright


load_dotenv()

BASE_URL = os.getenv("BASE_URL", "").rstrip("/") + "/"
LOGIN_PATH = os.getenv("LOGIN_PATH", "/index.php/login/validarUsuario")
USERNAME = os.getenv("USERNAME", "")
PASSWORD = os.getenv("PASSWORD", "")

OUT_BASE = Path("data/raw")
OUT_SHOTS = OUT_BASE / "screenshots"
OUT_RENDER = OUT_BASE / "rendered"
OUT_HAR = OUT_BASE / "har"

for p in (OUT_SHOTS, OUT_RENDER, OUT_HAR):
    p.mkdir(parents=True, exist_ok=True)


async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(base_url=BASE_URL)
        page = await context.new_page()

        # Login
        login_url = BASE_URL + LOGIN_PATH.lstrip("/")
        await page.goto(login_url)
        await page.fill("input[name='usuario']", USERNAME)
        await page.fill("input[name='pass']", PASSWORD)
        await page.click("button[type='submit'], input[type='submit']")
        await page.wait_for_timeout(2000)

        # Páginas de pacientes (paginación hasta 3)
        paths = [
            "/index.php/pacientes/index",
            "/index.php/pacientes/listar/2",
            "/index.php/pacientes/listar/3",
        ]

        for idx, path in enumerate(paths, start=1):
            await page.goto(path)
            await page.wait_for_timeout(1000)
            # Screenshot
            shot_path = OUT_SHOTS / f"pacientes_page_{idx}.png"
            await page.screenshot(path=str(shot_path), full_page=True)
            # HTML renderizado
            html_path = OUT_RENDER / f"pacientes_page_{idx}.html"
            html = await page.content()
            html_path.write_text(html, encoding="utf-8")
            # HAR opcional
            # (Playwright guarda HAR a nivel de contexto; para simplicidad, omitido aquí)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(capture())
