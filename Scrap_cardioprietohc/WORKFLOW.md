# Flujo de trabajo multi-puesto

Escenario: en casa podés acceder al sitio; en la oficina no. Mantén código y notas sincronizadas por git; mueve los datos scrapeados como snapshot (tar/rsync/USB/VPN).

## 1) Preparar cada máquina (una sola vez)
- `cd Scrap_cardioprietohc`
- `python -m venv .venv && source .venv/bin/activate`
- `pip install -r requirements.txt`
- Copia `.env.example` a `.env` y completa credenciales (solo en casa, no subas este archivo).

## 2) Ciclo de scraping en casa (tiene acceso al sitio)
- Activa el venv: `source .venv/bin/activate`.
- Ejecuta: `python -m scrap_cardioprietohc.cli run --target pacientes` (y/o `historias`).
- Se guardan HTML/JSON en `data/raw/` y logs en `data/logs/`.
- Generá índice RAG local (opcional): `python -m scrap_cardioprietohc.cli rag-index --source data/raw --index data/cache/rag_index.pkl`.
- Empaqueta lo que necesites llevar a la oficina (sin subirlo a git):
  - `tar -czf data_snapshot_$(date +%F).tar.gz data/raw data/logs`
  - Transfiere el `.tar.gz` por VPN/USB/rsync (ej: `rsync -av data_snapshot_*.tar.gz usuario@oficina:/ruta/omar-codex/Scrap_cardioprietohc/`).

## 3) Trabajo offline en la oficina
- Copia el snapshot y descomprímelo dentro de `Scrap_cardioprietohc`:
  - `tar -xzf data_snapshot_*.tar.gz`
- Analiza/parsea los HTML/JSON ya descargados; puedes iterar parsers sin tocar el sitio.
- Podés regenerar el índice RAG en la oficina: `python -m scrap_cardioprietohc.cli rag-index --source data/raw --index data/cache/rag_index.pkl`.
- Guarda hallazgos y pendientes en `SESSION_NOTES.md`.

## 4) Sincronización de código y notas (ambas máquinas)
- Usa git para código y notas (pero no para los dumps): `git add` de cambios en Python/MD; `git commit -m "scraper: avance parsers <fecha>"`.
- Al cambiar de máquina: `git pull` para traer código y `SESSION_NOTES.md`.
- Vuelve a casa, actualiza código/parseos y genera un nuevo snapshot si hace falta.

## 5) Cómo mantener “estado” entre sesiones
- Actualiza `SESSION_NOTES.md` al final de cada jornada con:
  - Qué endpoints/datos se scrapeó y dónde quedó el snapshot.
  - Qué parsers quedan pendientes o dudas sobre el sitio.
  - Qué cambiar en `client.py`/crawlers para el próximo intento.
- Si usas alguna cookie/token, guárdala en `data/cache/` (no en git) y describe su uso en las notas.
- Para consultas rápidas: `python -m scrap_cardioprietohc.cli rag-query --index data/cache/rag_index.pkl --query "texto"` (tras generar el índice).

## 6) Comandos útiles
- Activar venv: `source Scrap_cardioprietohc/.venv/bin/activate`
- Ejecutar scraper: `python -m scrap_cardioprietohc.cli run --target pacientes`
- Indexar RAG: `python -m scrap_cardioprietohc.cli rag-index --source data/raw --index data/cache/rag_index.pkl`
- Consultar RAG: `python -m scrap_cardioprietohc.cli rag-query --index data/cache/rag_index.pkl --query "campo paciente"`
- Empaquetar datos: `cd Scrap_cardioprietohc && tar -czf data_snapshot_$(date +%F).tar.gz data/raw data/logs`
- Restaurar snapshot: `cd Scrap_cardioprietohc && tar -xzf data_snapshot_YYYY-MM-DD.tar.gz`
