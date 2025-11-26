# Sesión - notas rápidas

- Se revisó el proyecto Django (`hhcc`, `ecocardiograma`) y las pautas de `CODEX.md`.
- Se acordó mantener separado el scraper bajo `Scrap_cardioprietohc/`.
- Se creó el scaffold del módulo de scraping:
  - `Scrap_cardioprietohc/requirements.txt` (crawl4ai, httpx, bs4, dotenv, opcional playwright).
  - `Scrap_cardioprietohc/.env.example` con BASE_URL/USERNAME/PASSWORD/OUTPUT_DIR.
  - Paquete `Scrap_cardioprietohc/Scrap_cardioprietohc/` con `config.py`, `client.py`, `pipelines.py`, `cli.py`, y crawlers stub `crawlers/pacientes.py`, `crawlers/historias.py`.
  - Carpetas `data/raw`, `data/cache`, `data/logs`.
- Comando de uso previsto (ajustar endpoints y credenciales reales):
  - `cd Scrap_cardioprietohc`
  - `pip install -r requirements.txt`
  - Copiar `.env.example` a `.env` y completar variables.
  - `python -m scrap_cardioprietohc.cli run --target pacientes` (o `historias`).

Pendientes para mañana
- Ajustar login real y rutas del sitio original en `client.py` y crawlers.
- Decidir si usar Playwright/crawl4ai para páginas con JS; instalar si hace falta.
- Implementar parseo real de tablas/detalles y diffs con modelos del nuevo sistema.
- Agregar logging y manejo de sesiones/cookies según el flujo del sitio.
