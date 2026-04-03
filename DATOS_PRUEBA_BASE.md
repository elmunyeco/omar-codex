# DATOS DE PRUEBA BASE (CRUD)

## Set de prueba creado
- Paciente:
  - `patient_id`: `11569`
  - `numDoc`: `999031799`
  - Nombre: `Test Integracion`
- Historia Clinica:
  - `historia_id`: `11565`

- Paciente (UI OK post-fix):
  - `patient_id`: `11570`
  - `numDoc`: `999031704`
  - Nombre: `Test2 Integracion`
- Historia Clinica (auto por signal):
  - `historia_id`: `11566`

## Operaciones realizadas (CUD no-estudios)
- **Create paciente (via UI)**: falla con `AttributeError` (`fechaalta` vs `fechaAlta`).
- **Create paciente (via UI, post-fix)**: OK (`patient_id 11570`).
- **Create paciente (via ORM, runtime)**:
  - Se desconecto el signal `crear_historia_clinica` para evitar error (solo en runtime).
  - Se creo paciente y se creo historia manualmente.
- **Update paciente**: POST a `/pacientes/11569/editar/` (telefono/localidad).
- **Update historia (signos/condiciones/comentarios)**:
  - POST JSON a `/api/historia/11565/guardar/` (status 200).
- **Create indicacion**:
  - POST JSON a `/historia/11565/indicaciones/agregar/` (id creado: `18621`).
- **Create comentario indicaciones**:
  - POST JSON a `/historia/11565/indicaciones/comentario/` (id creado: `15792`).
- **Delete indicacion**:
  - POST JSON a `/indicaciones/18621/eliminar/` (status 200).
- **Delete paciente**:
  - GET `/pacientes/11569/eliminar/` falla con `NoReverseMatch` (`detalle_paciente` inexistente).
  - Post-fix: GET `/pacientes/11570/eliminar/` OK, POST bloqueado (tiene historias).

## Notas
- Los endpoints de indicaciones usan CSRF inyectado en JS (no via input hidden).
- El signal `crear_historia_clinica` en `/home/eze/omar/hhcc/main/signals.py` usa `fechaalta`
  (deberia ser `fechaAlta`) y rompe el alta via UI/ORM normal.
