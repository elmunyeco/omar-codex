# Scrap_cardioprietohc

Estructura separada para scrapear el sistema original y comparar con el nuevo código.

## Requisitos
- Python 3.10+
- (Opcional) Playwright si el sitio requiere JS intensivo.

Instala dependencias (sin entorno virtual aquí, ajusta a tu flujo):
```bash
pip install -r requirements.txt
# Si usás Playwright
python -m playwright install chromium
```

## Configuración
Copia `.env.example` a `.env` y completa las credenciales del sitio original.

Variables:
- `BASE_URL`: URL base del sistema original.
- `USERNAME`, `PASSWORD`: credenciales de login.
- `OUTPUT_DIR`: carpeta donde guardar los dumps (`data/raw` por defecto).

## Uso rápido
```bash
# Pacientes
python -m scrap_cardioprietohc.cli run --target pacientes

# Historias
python -m scrap_cardioprietohc.cli run --target historias

# RAG: indexar y consultar lo scrapeado
python -m scrap_cardioprietohc.cli rag-index --source data/raw --index data/cache/rag_index.pkl
python -m scrap_cardioprietohc.cli rag-query --index data/cache/rag_index.pkl --query "nombre de campo"
```

Los HTML y JSON quedan en `data/raw/` y los logs en `data/logs/`.

## Flujo multi-puesto (casa/oficina)
- Configurá un venv por máquina (`python -m venv .venv && source .venv/bin/activate`).
- En casa (con acceso al sitio) corré el scraper y empaquetá `data/raw` + `data/logs` en un `data_snapshot_*.tar.gz` (ver `WORKFLOW.md` para comandos).
- Transferí el snapshot por VPN/USB y extráelo en la oficina; allí seguís con el parseo sin tocar internet.
- Sincronizá código y `SESSION_NOTES.md` por git; no subas los snapshots ni `.env`.
- El índice RAG (por defecto `data/cache/rag_index.pkl`) no se sube a git; podés regenerarlo en cada máquina desde `data/raw`.
