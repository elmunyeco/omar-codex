# HISTORIAL MEDICO BASE (solo lectura)

## Ubicacion
- Template principal: `main/templates/detalle_historia_con_historial.html`
- Alternativa: `detalle_historia_con_historial_2.html`
- Server: `http://127.0.0.1:8080`

## Endpoint
- `/historial_medico/<historia_id>/` (GET)

## Estructura de UI (scrape GET)
- Secciones principales detectadas por encabezados:
  - `Signos Vitales`
  - `Condiciones Médicas`
  - `Historial de Visitas Médicas`
- Botonera:
  - `Medicación` -> `/historia/<historia_id>/indicaciones/`
  - `Prácticas` -> `/ordenes_medicas/<historia_id>/`
  - `Imprimir` -> `window.print()`

## JS / Alpine (scrape GET)
- Usa Alpine con `x-data`:
  - Estado: `signos_vitales` (presion sistolica/diastolica, peso, glucemia, colesterol)
  - `condiciones` como Set
  - `comentarios`
  - `cambios_pendientes` y `errorMessage`
- Persistencia:
  - POST JSON a `/api/historia/<historia_id>/guardar/`
  - En exito: recarga pagina
  - En error: muestra `errorMessage`

## Diferencias entre templates
- `detalle_historia_con_historial.html` es HTML completo (no hereda `base.html`).
- `detalle_historia_con_historial_2.html` **extiende** `base.html` y redefine estilos locales
  (reset de `container-content` y `page-content`).
- Estructura funcional es casi identica; `_2` está mejor alineado al layout base.

## Campos (x-model)
- `estado.signos_vitales.presion_sistolica`
- `estado.signos_vitales.presion_diastolica`
- `estado.signos_vitales.peso`
- `estado.signos_vitales.glucemia`
- `estado.signos_vitales.colesterol`
- `estado.comentarios`
- Condiciones: checkboxes (25 en el scrape)

## Observaciones de integracion
- Este flujo es el punto natural de acople con estudios (links a estudios, contexto paciente).
- Los estilos usan Tailwind CDN + `static/main/css/style.css`.
- Regla: ante discrepancias de estilos/estructura compartida, **prevalece omar-codex**.
