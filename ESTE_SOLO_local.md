# Contexto local (servidor nuevo http://localhost:8080) – Solo lectura/scrape

## Ubicación de dumps
- `/home/eze/omar/scrap_local_8080/data/raw/`:
  - `pacientes_list.html`
  - `pacientes_edit_11564.html`
  - `pacientes_crear.html`
  - `historias_list.html`
  - `historial_medico_11564.html`
- Assets descargados desde `pacientes_list.html`: `data/raw/assets/static/main/css/style.css`, `.../js/components/header.js`, `.../images/logo.png`, y un intento de `https://cdn.tailwindcss.com` (403, no guardado). También `alpinejs` desde unpkg guardado como `https:/unpkg.com/...` (por la URL sin esquema correcto en el guardado).

## Cómo se obtuvieron
- Sin login (el server no tiene auth). Comandos usados:
  - `curl -L http://localhost:8080/pacientes/ -o data/raw/pacientes_list.html`
  - `curl -L http://localhost:8080/pacientes/11564/editar/ -o data/raw/pacientes_edit_11564.html`
  - `curl -L http://localhost:8080/pacientes/crear/ -o data/raw/pacientes_crear.html`
  - `curl -L http://localhost:8080/historias/ -o data/raw/historias_list.html`
  - `curl -L http://localhost:8080/historial_medico/11564/ -o data/raw/historial_medico_11564.html`
- Parsing rápido (HTMLParser) de `pacientes_list.html` para obtener links de edición (IDs 11564, 11563, ...). Parsing de `historias_list.html` para obtener links `/historial_medico/<id>/`.
- Asset download (sin requests/bs4, usando urllib): falló tailwind CDN (403); se guardaron CSS/JS estáticos locales y logo.

## Pendientes (para próxima sesión)
- Instalar deps si se quiere indexar RAG aquí (no hay pip en sistema; crear venv propio si hace falta).
- Completar descarga de assets faltantes (tailwind CDN) si se requiere reproducir UI exacta; o servir tailwind local.
- Añadir scraping de otras vistas si es necesario (paginaciones, etc.) siguiendo el mismo patrón con `curl`.
