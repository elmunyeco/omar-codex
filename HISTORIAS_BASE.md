# HISTORIAS CLINICAS BASE (solo lectura)

## Ubicacion
- Proyecto base: `/home/eze/omar/hhcc`
- Templates: `/home/eze/omar/hhcc/main/templates/`
- Server: `http://127.0.0.1:8080`

## Endpoints
- Listado/busqueda: `/historias/` (GET)
- Historial medico: `/historial_medico/<historia_id>/` (GET)

## Templates principales
- Listado: `listar_buscar_historias_2.html`
- Historial medico: `detalle_historia_con_historial.html` y `detalle_historia_con_historial_2.html`
- Carpeta auxiliar: `main/templates/historial_medico/` (`historial_medico.html`, `h1.html`, `h2.html`, `h3.html`)
- `ver_estudios.html` existe pero esta vacio (0 bytes).

## Formulario (GET scrape)
- Busqueda (GET):
  - Campos: `query`, `tipo` (ID/Documento/Nombre/Apellido)
- Historial medico: page GET sin form visible (usa JS/partials).

## Modelos (referencia)
- `HistoriaClinica` (FK a `Paciente`)
- `SignosVitales`
- `ComentariosVisitas` (tipo: EVOL/INDIC)

## Observaciones de integracion
- Falta mapear flujo completo del historial medico (secciones, acciones, JS).
- Al integrar con estudios, el punto natural de acople es el historial medico
  (links a estudios, contexto del paciente y HC).
- Regla: ante discrepancias de estilos/estructura compartida, **prevalece omar-codex**.
