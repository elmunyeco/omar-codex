# LISTADOS BASE (pacientes e historias)

## Pacientes (listar_buscar_pacientes.html)
- Endpoint: `/pacientes/` (GET)
- Busqueda:
  - `query` (texto)
  - `tipo` (Documento/Nombre/Apellido)
- Tabla:
  - Columnas: Nombre, Apellido, Documento, Acciones
  - Accion: editar (`/pacientes/<id>/editar/`)
- Discrepancia detectada: usa `{{ paciente.dni }}` en tabla (debe ser `numDoc`).
- Paginacion con query string.
- Breadcrumbs eliminados (regla global).

## Historias (listar_buscar_historias_2.html)
- Endpoint: `/historias/` (GET)
- Busqueda:
  - `query` (texto)
  - `tipo` (ID/Documento/Nombre/Apellido)
- Tabla:
  - Columnas: Id Historia, Nombre, Apellido, Documento, Acciones
  - Accion: editar historia (`/historial_medico/<id>/`)
- Accion: “Ver estudios” apunta a `/` (placeholder).
- Paginacion con query string.
- Breadcrumbs eliminados (regla global).

## Observaciones de integracion
- Alinear listados con `omar-codex` (fuente mas nueva).
- Regla UI global: **breadcrumbs se eliminan en todo el sistema**.
