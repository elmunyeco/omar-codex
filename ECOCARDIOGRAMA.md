# ECOCARDIOGRAMA (impresión)

## Base de impresión
- El template de impresión extiende `print_base.html` para homogeneidad.
- Usa logo, site y header parametrizados via contexto.
- `print_base.html` carga `print.css` para estilos comunes.

## Estilo sin Tailwind
- Se removieron clases Tailwind en impresión.
- El layout usa CSS propio (tablas, grilla, firma, botones de impresión).
- Títulos y secciones usan los mismos separadores y jerarquía que carótidas.

## Archivos clave
- `hhcc/ecocardiograma/templates/ecocardiograma/imprimir_estudio.html`
- `hhcc/ecocardiograma/views.py` (pasa `print_logo_path`, `print_site_text`, `print_header_text`).
