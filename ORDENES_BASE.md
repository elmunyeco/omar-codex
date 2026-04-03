# ORDENES MEDICAS/PEDICAS BASE (solo lectura)

## Ubicacion
- Proyecto base: `/home/eze/omar/hhcc`
- Templates: `/home/eze/omar/hhcc/main/templates/`
- Server: `http://127.0.0.1:8080`

## Endpoints
- Ordenes medicas: `/ordenes_medicas/<paciente_id>/`
- Ordenes pedicas: `/ordenes_pedicas/<paciente_id>/`
- Generar PDF: `/generar_pdf_orden/<paciente_id>/<diagnostico>/<estudios>/<tipo>/`
- Descargar PDF: `/descargarPDFSolicitudes/<paciente_id>/<diagnostico>/<estudios>/<tipo>/`

## Estado (scrape GET)
- `ordenes_medicas/0/` y `ordenes_pedicas/0/` devolvieron 404 (requiere `paciente_id` valido).
- `ordenes_medicas/11564/` y `ordenes_pedicas/11564/` devuelven HTML valido (GET).

## UI / JS (scrape GET)
- Ambas pantallas usan Alpine (`x-data`).
- Flujo principal:
  - Seleccion de estudios via checkboxes (116 en `ordenes_medicas`).
  - Campo `diagnostico` y `otrosEstudios` (textarea).
  - `imprimirOrdenes()` abre PDFs via `window.open()`:
    - En **ordenes_medicas**: `/descargarPDFSolicitudes/<paciente_id>/<diagnostico>/<lista_ids>/<grupo>/`
    - En **ordenes_pedicas**: `/generar_pdf_orden/<paciente_id>/<diagnostico>/<lista_ids>/<grupo>/`
  - Mensaje de error si no se selecciona ningun estudio.
- Botones: `Imprimir Órdenes` y `Cancelar`.
- `Prácticas` en historial medico apunta a `/ordenes_medicas/<historia_id>/`.
- Lista de estudios de laboratorio/cardio/clinicos embebida en HTML.

## Observaciones de integracion
- Falta relevar templates y JS con un `paciente_id` existente.
- Regla: ante discrepancias de estilos/estructura compartida, **prevalece omar-codex**.
