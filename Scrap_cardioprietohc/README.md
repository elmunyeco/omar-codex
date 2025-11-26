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
```

Los HTML y JSON quedan en `data/raw/` y los logs en `data/logs/`.
