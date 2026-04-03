# INDICACIONES BASE (solo lectura)

## Ubicacion
- Proyecto base: `/home/eze/omar/hhcc`
- Templates: `/home/eze/omar/hhcc/main/templates/indicaciones/`
- Server: `http://127.0.0.1:8080`

## Endpoints
- Listado: `/historia/<historia_id>/indicaciones/` (GET)
- Agregar: `/historia/<historia_id>/indicaciones/agregar/` (GET/POST JSON via fetch)
- Eliminar: `/indicaciones/<id>/eliminar/`
- Comentarios (historia): `/historia/<historia_id>/indicaciones/comentario/`
- API: `/api/historia/<historia_id>/ultimos-comentarios/`

## Templates principales
- Lista: `indicaciones/lista.html`
- Agregar: `indicaciones/agregar.html`
- Base: `indicaciones/base.html`

## Comportamiento (scrape GET)
- La pagina de agregar usa Alpine y un formulario sin `action` HTML:
  - Envia POST JSON via `fetch('/historia/<id>/indicaciones/agregar/')`.
  - Campos en JS: `medicamento`, `ochoHoras`, `doceHoras`, `dieciochoHoras`, `veintiunaHoras`, `fecha`.
  - Valida que `medicamento` no este vacio.
  - En exito: muestra mensaje y redirige a `/historia/<id>/indicaciones/`.
  - En error: muestra mensaje y queda en pagina.
- La lista usa Alpine para:
  - Eliminar indicaciones via POST JSON a `/indicaciones/<id>/eliminar/`.
  - Guardar comentario via POST JSON a `/historia/<id>/indicaciones/comentario/`.
  - Controlar `cambiosPendientes` comparando contra copia local.

## Modelos (referencia)
- `IndicacionesVisitas` (medicamento + cuatro horarios + fecha + eliminado).
- `ComentariosVisitas` para notas asociadas.

## Observaciones de integracion
- Esta UI usa JS/Alpine; hay que alinear estilos con omar-codex.
- Regla: ante discrepancias de estilos/estructura compartida, **prevalece omar-codex**.
