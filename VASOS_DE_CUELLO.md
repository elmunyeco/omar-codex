# VASOS_DE_CUELLO (Carótidas)

## Impresión (PDF)
- La impresión se genera como PDF con WeasyPrint (no HTML).
- Endpoint: `/carotidas/imprimir_estudio/<estudio_id>/<historia_id>/`.
- Respuesta `Content-Type: application/pdf` y `Content-Disposition: inline`.
- Se ocultan secciones sin datos (no imprime títulos vacíos).
- Logo incluido desde `Scrap_cardioprietohc/data/raw/carotidas/assets/images/logo.jpg`.
- Sitio en header: `www.cardioprietohc.com`.
- Texto corregido sin errores ortográficos (p.ej. “Quality Intima Media Thickness Analysis”).
- No se imprime “Consultorio Cardiológico Doctores Prieto”; usar “Consultorio Cardiológico Doctor Omar Prieto” (en alt del logo y/o texto visible).

## UX / comportamiento
- Submit AJAX: guarda y abre nueva ventana con el PDF.
- Popup se abre antes del fetch para evitar bloqueos.
- Comentarios en carótida común solo visibles si se elige “Otras”.
- Sub‑opciones solo visibles si se elige “Se observa lesión”.
- Vertebrales: sub‑opciones Izq/Der solo si se elige “Disminución del flujo…”.
- Pre‑informe en vivo con Alpine.
- Botones “Limpiar” por bloque.
- Validación espesor íntima‑media (regex + coma→punto).

## Archivos clave
- `hhcc/carotidas/templates/carotidas/nuevo_estudio.html`
- `hhcc/carotidas/templates/carotidas/imprimir_estudio.html`
- `hhcc/carotidas/views.py`
- `hhcc/carotidas/urls.py`

## Referencias legacy
- PDF legacy descargado: `Scrap_cardioprietohc/data/raw/carotidas/imprimirEstudio_4512_7544.pdf`.


## Template base de impresión
- Base compartida: `hhcc/main/templates/print_base.html`.
- Incluye logo, site, meta, y divisores suaves.
- `imprimir_estudio.html` ahora extiende `print_base.html`.
- Se agregaron líneas horizontales suaves entre membrete/títulos y títulos/informe.


- Base compartida parametrizada con `print_logo_path`, `print_site_text`, `print_header_text`.


- Usa `print.css` via `print_base.html`.
