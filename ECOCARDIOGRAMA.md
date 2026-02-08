# ECOCARDIOGRAMA (impresión)

## Base de impresión
- El template de impresión extiende `print_base.html` para homogeneidad.
- Usa logo, site y header parametrizados via contexto.

## Estilo sin Tailwind
- Se removieron clases Tailwind en impresión.
- El layout usa CSS propio dentro del template (tablas, grilla, firma, etc.).

## Archivos clave
- `hhcc/ecocardiograma/templates/ecocardiograma/imprimir_estudio.html`
- `hhcc/ecocardiograma/views.py` (pasa `print_logo_path`, `print_site_text`, `print_header_text`).


- Usa `print.css` via `print_base.html`.
- Títulos y secciones usan mismos separadores que carótidas.
