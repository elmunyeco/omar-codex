# INTEGRACION HHCC BASE (solo lectura)

## Contexto y objetivo
- Este documento cataloga el sistema base (historias clinicas/pacientes/indicaciones/visitas) ubicado en `/home/eze/omar`.
- Objetivo: preparar la integracion organica con el prototipo de estudios del sandbox (`/home/eze/omar-codex/hhcc`).
- Regla actual: **solo lectura**. Scrape permitido solo GET. CUD requiere aviso previo.
- Directiva de integracion: cuando haya discrepancias en estilos, templates o arquitectura compartida,
  **prevalece lo implementado en `/home/eze/omar-codex`** por ser la version mas nueva.
- Regla de reemplazo de estudios: todo lo relacionado a **carotidas, doppler/MMII y stress/ecostress**
  en `/home/eze/omar` o en MySQL sera **reemplazado** por lo ya implementado en `/home/eze/omar-codex`.
  Ademas, se **agrega** ecocardiograma desde `/home/eze/omar-codex`.

## Ubicacion y servidor
- Directorio base: `/home/eze/omar`.
- Proyecto Django principal: `/home/eze/omar/hhcc`.
- Server local: `http://127.0.0.1:8080` (sin auth).

## Settings (Django base)
- Archivo: `/home/eze/omar/hhcc/hhcc/settings.py`.
- Apps instaladas: `main`, `ecocardiograma`, `earthbox`.
- DB default: MySQL `cardioprieto` en `127.0.0.1:3307` (user `root`).
- `CORS_ALLOW_ALL_ORIGINS = True`, `X_FRAME_OPTIONS = ALLOWALL`.

## URLs (Django base)
- Archivo: `/home/eze/omar/hhcc/hhcc/urls.py`.
- Monta:
  - `''` -> `main.urls`
  - `/ecocardiograma/` -> `ecocardiograma.urls`
  - `/earthbox/` -> `earthbox.urls`

### Endpoints principales (main.urls)
- `/` (index)
- `/landing/`, `/landing_dropdown/`, `/buscador/`
- `/pacientes/` (listar/buscar)
- `/pacientes/crear/`
- `/pacientes/<id>/editar/`
- `/pacientes/<id>/eliminar/`
- `/historias/` (listar/buscar)
- `/historial_medico/<historia_id>/`
- `/historia/<historia_id>/indicaciones/`
- `/historia/<historia_id>/indicaciones/agregar/`
- `/indicaciones/<id>/eliminar/`
- `/historia/<historia_id>/indicaciones/comentario/`
- `/api/historia/<historia_id>/ultimos-comentarios/`
- `/api/historia/<historia_id>/guardar/`
- `/ordenes_medicas/<paciente_id>/`
- `/ordenes_pedicas/<paciente_id>/`
- `/generar_pdf_orden/<paciente_id>/<diagnostico>/<estudios>/<tipo>/`
- `/descargarPDFSolicitudes/<paciente_id>/<diagnostico>/<estudios>/<tipo>/`
- Ejemplos: `/h1/`, `/h2/`, `/h3/`

## Modelos clave (main.models)
- `Paciente`: datos personales, doc, sexo H/M, fechaAlta, deBaja.
- `HistoriaClinica`: FK a `Paciente`, fechaAlta, condiciones.
- `CondicionMedica`, `CondicionMedicaHistoria` (M2M).
- `SignosVitales`.
- `ComentariosVisitas` (Evolucion/Indicaciones).
- `IndicacionesVisitas`.

## Scrape (solo lectura, GET)
- `/` muestra enlaces a pacientes/historias/ordenes.
- `/pacientes/` expone lista con links a editar pacientes.
- `/historias/` expone lista con links a historial medico.
- `/historia/<id>/indicaciones/` ofrece link a agregar indicacion.
- No se hicieron POST/PUT/DELETE.

## Earthbox
- App minima para pruebas.
- URLs: `/earthbox/` y `/earthbox/echo/?q=...`.

## Notas de integracion (pendiente)
- Falta mapear templates y flujos reales de:
  - Historial medico (detalle + comentarios).
  - Indicaciones (listado, alta, comentarios, eliminacion).
  - Ordenes medicas/pedicas y PDFs.
- Verificar compatibilidad UI/UX con prototipo de estudios.
- Identificar puntos de acople:
  - Desde historial medico a estudios (links, contexto de paciente).
  - Reutilizacion de header/layout global.
  - Estilos compartidos y static assets.

## Proximo paso sugerido
1. Catalogar templates principales de `main/templates` (solo lectura).
2. Scrape GET de `historial_medico/<id>` y `indicaciones` (HTML guardado).
3. Crear un mapa de datos (campos reales en HTML + JS).
4. Relevamiento de endpoints de ordenes y PDFs.
