# RELEVAMIENTO BASE (resumen operativo)

## Alcance actual (solo lectura)
- Proyecto base: `/home/eze/omar/hhcc` (Django + MySQL).
- Server: `http://127.0.0.1:8080`.
- Scrape GET guardado en: `/home/eze/omar-codex/scrap_local_8080_base/`.
- DB inspeccionada en solo lectura (MySQL `cardioprieto`).

## Lo relevado (templates/flujo/UI)
- Base UI:
  - `base.html` + `components/header.html` + `static/main/css/style.css` + `static/main/js/components/header.js`.
  - Menu principal, submenus, logout a `/logout/`.
  - Breadcrumbs existen pero **se van a eliminar** (regla global).
- Pacientes:
  - Listado/busqueda (`listar_buscar_pacientes.html`).
  - Crear (`crear_paciente.html`) y Editar (`editar_paciente.html`).
  - Eliminar (`eliminar_paciente.html`) y Detalle (template antiguo `detalle_paciente.html`).
- Historias:
  - Listado (`listar_buscar_historias_2.html`).
  - Historial medico (`detalle_historia_con_historial.html` y `_2.html`).
  - `ver_estudios.html` existe pero está vacío.
- Indicaciones:
  - Lista (`indicaciones/lista.html`) con Alpine + fetch (eliminar y guardar comentario).
  - Agregar (`indicaciones/agregar.html`) con POST JSON via fetch.
- Ordenes:
  - `ordenes_medicas.html` usa `/descargarPDFSolicitudes/...`.
  - `ordenes_pedicas.html` usa `/generar_pdf_orden/...`.

## DB (MySQL)
- Tablas core: `pacientes`, `historias_clinicas`, `signos_vitales`, `comentarios_visitas`, `indicaciones_visitas`, `condiciones_medicas*`.
- Estudios legacy en DB: `carotidas`, `doppler`, `stress` (a reemplazar por omar-codex).

## Discrepancias detectadas (a corregir hacia omar-codex)
- `listar_buscar_pacientes.html` usa `paciente.dni` (debe ser `numDoc`).
- Sexo en forms usa `M/F`, pero modelo usa `H/M`.
- Breadcrumbs presentes (se eliminan globalmente).
- `detalle_paciente.html` parece plantilla vieja (Bootstrap, campos no actuales).
- `ver_estudios.html` vacío (debe integrarse con estudios de omar-codex).
- Alta de paciente falla: `AttributeError` por uso de `fechaalta` en signal.
- Eliminar paciente falla: `NoReverseMatch` (`detalle_paciente` no existe).

## Correcciones aplicadas en omar (base)
- Signal `crear_historia_clinica`: usa `fechaAlta` (fix del alta).
- Listado pacientes: usa `numDoc`.
- Sexo en forms: `H/M`.
- Breadcrumbs eliminados de header y listados.
- Eliminar paciente: link de cancelar corregido y bloqueo si tiene historias.

## Qué falta relevar
- `landing*`, `buscador.html`, `historial_medico/*.html` auxiliares.
- `main/static/main/css/style.css` comparado contra omar-codex (ajustes de estilo).
- Flujos completos de CRUD (crear/editar/eliminar) en pacientes e historias con datos reales.
- APIs: respuestas reales de `/api/historia/<id>/guardar/` y `/api/.../ultimos-comentarios/`.

## Regla de integración
- **Estudios**: carótidas, doppler/MMII, stress/ecostress se reemplazan por omar-codex.
- Se **agrega** ecocardiograma desde omar-codex.
- Discrepancias UI/arquitectura comunes se resuelven hacia **omar-codex**.
