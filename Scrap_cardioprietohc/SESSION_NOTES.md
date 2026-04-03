# Session Notes

Fecha: 2026-03-24

## Hecho
- Migración de signos vitales desde legacy (3308 `signosvitales`) a local (3307 `signos_vitales`) con `REPLACE`.
  - Se clampeó `peso > 999.99` a `999.99` (caso legacy `idHC=709`, `peso=1104`).
- Matriz funcional generada y documentada:
  - `Scrap_cardioprietohc/data/reports/functional_matrix_report.md` y PDF.
- Prueba de idempotencia UI (ID 7544) ejecutada:
  - `Scrap_cardioprietohc/data/reports/idempotency_ui_7544.md`
- Fix aplicado (local live + repo): comentarios de evolución no aparecían por filtro de fecha en `DateTimeField`.
  - Se reemplazó por **rango UTC** (`fecha__gte`/`fecha__lt`) y se corrigió `fecha_visita` en `guardar_historia`.
  - Resultado: el comentario del día **ya se muestra** en la UI.
- Documentación refinada con reglas operativas y criterio de fecha de comentarios (día).
- Mapa de pantallas core (legacy vs local) con alcance de idempotencia por pantalla:
  - `Scrap_cardioprietohc/data/reports/pantallas_core_map_2026-03-24.md`

## Pendientes
- Validar nuevamente el PDF de la matriz funcional si se actualiza.
- Criterio funcional: una sola visita por día. Si se detectaran dos visitas el mismo día, consultar al médico; por defecto se edita la primera.
- Regla adicional: fecha de comentarios con precisión **día** es suficiente (no se requiere hora).
- Idempotencia debe validarse **solo por UI** usando **exclusivamente** ID 7544.
- El test de idempotencia core **excluye** módulos de estudios (pendiente integración local + local‑estudios).
- Depuración urgente antes de integrar/entregar: coexistencia de múltiples plantillas de HC
  (`hhcc/main/templates/detalle_historia_con_historial*.html`, incluido `_2`) sugiere duplicidad/incompletitud que debe resolverse.
- Órdenes: `ordenes_pedicas` parece la versión funcional/reciente (usa `generar_pdf_orden` + manejo de "otros estudios").
  `ordenes_medicas` usa `descargarPDFSolicitudes` y tiene bug (usa `url` no definido para "otros estudios").
  Acción: unificar/redirect de `ordenes_medicas` → `ordenes_pedicas` y limpiar menú/plantillas duplicadas.
- Documento de cobertura legacy vs local (con evidencia visual, agrupado por pantalla):
  - `Scrap_cardioprietohc/data/reports/legacy_vs_local_use_cases_2026-03-26.md`
  - PDF: `Scrap_cardioprietohc/data/reports/legacy_vs_local_use_cases_2026-03-26.pdf`
- Pipeline de PDF para el documento de cobertura:
  - Fuente editable: `Scrap_cardioprietohc/data/reports/legacy_vs_local_use_cases_2026-03-26.src.md`
  - Script (no trackeado): `/home/eze/omar-codex/render_legacy_vs_local.sh`
- Plan de cierre local documentado:
  - `Scrap_cardioprietohc/data/reports/plan_cierre_local_2026-03-26.md`
- TODO (auth): mostrar nombre del usuario autenticado en el header (no fijo).
- TODO (auth): definir política final de contraseñas (en local se deshabilitaron validadores).

## Archivos clave
- Fix: `hhcc/main/views.py`
- Reportes:
  - `Scrap_cardioprietohc/data/reports/functional_matrix_report.md`
  - `Scrap_cardioprietohc/data/reports/functional_matrix_report.pdf`
  - `Scrap_cardioprietohc/data/reports/idempotency_ui_7544.md`
  - `Scrap_cardioprietohc/data/reports/signos_vitales_clamped_legacy.tsv`

---

Fecha: 2026-04-03

## Hecho
- Integrado `auth-minima` en `consolidacion` (repo `/home/eze/omar`).
  - Login/Logout funcional, cambio de contraseña, cambio de nombre completo.
  - Header simplificado: solo nombre + logout; logo abre mini‑perfil.
  - Logout arreglado (GET/POST, sin 405).
- QA funcional (E) con usuario `omar` en local `http://127.0.0.1:8080`.
  - Pacientes: crear/editar OK.
  - Historias: listado + paginación OK.
  - HC detalle: guardar OK (signos/condiciones/comentarios), comentarios JSON OK.
  - Indicaciones: agregar + eliminar OK.
- Idempotencia UI (F) con CDP legacy + local:
  - Reportes: `Scrap_cardioprietohc/data/reports/idempotency_ui_7544.json` y `.md`.
  - Legacy: comentarios NO idempotentes (duplica). Signos sin cambio.
  - Local: comentario/visitas idempotentes en segunda pasada.

## Bloqueos / Notas
- Eliminación de paciente con HC asociada bloqueada por diseño (no se cambia por motivos legales).
  - `TEST_QA_2` creado y no se pudo eliminar por HC asociada.
  - Intento de borrar HC falla por dependencia a tabla `estudios_ecocardiograma` inexistente en DB local.
- `TEST_QA_1` creado y editado (obraSocial=QA_OBRA, telefono=123456). Se deja en base.

## Pendientes
- Continuar checklist desde G (documentación) y H (integración estudios).
- Definir política final de contraseñas (en local se deshabilitaron validadores).
- Resolver dependencia DB de `estudios_ecocardiograma` si se necesita borrar HC en QA.

## Importante para próxima sesión
- Leer **toda** la documentación en `/home/eze/omar-codex/Scrap_cardioprietohc/data/reports/` antes de integrar.
- La próxima sesión **integra** `/home/eze/omar-codex` con `/home/eze/omar`.

