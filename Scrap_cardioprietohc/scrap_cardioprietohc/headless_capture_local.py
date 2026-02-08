"""
Headless capture para el servidor local (ej: http://localhost:8080).
Usa Playwright con --no-sandbox para evitar restricciones en entornos sin sandbox.
"""
import asyncio
from pathlib import Path
from urllib.parse import urljoin

from playwright.async_api import async_playwright

BASE_URL = "http://localhost:8080/"
PACIENTES_PATHS = [
    "/pacientes/",
    "/pacientes/?page=2",
    "/pacientes/?page=3",
]
OUT_SHOTS = Path("data/raw/screenshots_local")
OUT_RENDER = Path("data/raw/rendered_local")
for p in (OUT_SHOTS, OUT_RENDER):
    p.mkdir(parents=True, exist_ok=True)


async def capture_local():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = await browser.new_page(base_url=BASE_URL)

        for idx, path in enumerate(PACIENTES_PATHS, start=1):
            url = urljoin(BASE_URL, path.lstrip("/"))
            print(f"GET {url}")
            await page.goto(url)
            await page.wait_for_timeout(1000)
            shot = OUT_SHOTS / f"local_pacientes_{idx}.png"
            await page.screenshot(path=str(shot), full_page=True)
            html_path = OUT_RENDER / f"local_pacientes_{idx}.html"
            html_path.write_text(await page.content(), encoding="utf-8")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(capture_local())
