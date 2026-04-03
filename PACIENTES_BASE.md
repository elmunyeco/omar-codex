# PACIENTES BASE (solo lectura)

## Ubicacion
- Proyecto base: `/home/eze/omar/hhcc`
- Templates: `/home/eze/omar/hhcc/main/templates/`
- Server: `http://127.0.0.1:8080`

## Endpoints
- Listado/busqueda: `/pacientes/` (GET)
- Crear: `/pacientes/crear/` (GET/POST)
- Editar: `/pacientes/<id>/editar/` (GET/POST)
- Eliminar: `/pacientes/<id>/eliminar/` (GET/POST)

## Templates principales
- Listado: `listar_buscar_pacientes.html`
- Crear: `crear_paciente.html`
- Editar: `editar_paciente.html`
- Eliminar: `eliminar_paciente.html`
- Detalle: `detalle_paciente.html`

## Formulario (GET scrape)
- Busqueda (GET):
  - Campos: `query`, `tipo`
- Crear/Editar (POST tradicional):
  - Campos vistos en HTML: `idTipoDoc`, `numDoc`, `nombre`, `apellido`, `fechaNac`, `sexo`, `mail`,
    `telefono`, `celular`, `direccion`, `localidad`, `obraSocial`, `plan`, `afiliado`, `profesion`, `referente`
  - CSRF incluido (Django standard)

## Discrepancias detectadas
- `listar_buscar_pacientes.html` muestra `{{ paciente.dni }}` en vez de `{{ paciente.numDoc }}`.
- Formularios de crear/editar usan valores de sexo `M/F`, pero el modelo usa `H/M`.
  (debe resolverse hacia omar-codex).
- Alta de paciente falla por `AttributeError` (`fechaalta` vs `fechaAlta`) en signal.
- Eliminar paciente falla por `NoReverseMatch` (`detalle_paciente` no existe).

## Estado actual (post-fix)
- `numDoc` corregido en listado.
- Sexo corregido a `H/M` en formularios.
- Signal `crear_historia_clinica` corregido (`fechaAlta`).
- Eliminar paciente muestra warning y bloquea borrado si hay historias.

## Modelos (referencia)
- `Paciente` en `/home/eze/omar/hhcc/main/models.py`
- Sexo: `H/M` (Hombre/Mujer)
- `numDoc` y `idTipoDoc` (FK a `TipoDocumento`)

## Observaciones de integracion
- El sandbox (`/home/eze/omar-codex`) ya ajusto UI/UX de estudios.
- Regla: si hay discrepancias en estilos/estructura compartida, **prevalece omar-codex**.
