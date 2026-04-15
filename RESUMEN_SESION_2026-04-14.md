# Resumen de sesion 2026-04-14

## Regla de contexto permanente
- `/home/eze/omar-codex` y `/home/eze/omar` son dos repositorios del mismo negocio.
- Cualquier analisis o cambio debe considerar ambos repos como un contexto unico y asociado de forma permanente.
- Esto ya quedo documentado en:
  - `/home/eze/omar-codex/CONTEXTO.md`
  - `/home/eze/omar/INTEGRACION_NOTAS.md`

## Trabajo realizado sobre DB y migraciones
- Se comparo el esquema real de MySQL `cardioprieto` en `127.0.0.1:3307` contra dumps de referencia.
- Se valido en un sandbox MySQL aparte (`3310`, contenedor `codex_sandbox_db`) que las migraciones originales no reproducian exactamente el esquema objetivo.
- Se implemento convergencia de esquema en:
  - `/home/eze/omar-codex/hhcc/main/models.py`
  - `/home/eze/omar-codex/hhcc/main/migrations/0001_recreate_clean.py`
  - `/home/eze/omar-codex/hhcc/main/migrations/0003_rename_idpaciente_idx_historia_paciente_idx_and_more.py`
  - `/home/eze/omar-codex/hhcc/main/migrations/0004_schema_target_alignment.py`
- `main.0004_schema_target_alignment` ya fue aplicada en la DB real `3307`.

## Resultado actual del esquema real
- Se borraron las tablas legacy:
  - `comentarios`
  - `random_hc`
- Se unifico collation a `utf8mb4_uca1400_ai_ci` en tablas del proyecto y tablas Django/auth relevantes.
- `pacientes` quedo con:
  - `obraSocial`, `afiliado`, `telefono`, `celular`, `profesion` en `NULL`
  - `FULLTEXT nombre_apellido_idx`
  - sin `unique_together (idTipoDoc_id, numDoc)` a nivel de modelo/estado
- `indicaciones_visitas` quedo con:
  - FK a `historias_clinicas`
  - indice `indicaciones_fecha_idx`
  - collation `utf8mb4_uca1400_ai_ci`

## Tablas de negocio actuales
- `carotidas`
- `comentarios_visitas`
- `conclusiones_ecocardiograma`
- `condiciones_medicas`
- `condiciones_medicas_historias`
- `estudios_ecocardiograma`
- `historias_clinicas`
- `indicaciones_visitas`
- `mmii`
- `pacientes`
- `segmentos_ecocardiograma`
- `signos_vitales`
- `stress`
- `tipos_documentos`

## Docker / deploy
- Se ajusto el arranque de la app Docker para usar MySQL real y correr migraciones al inicio:
  - `/home/eze/omar-codex/Dockerfile`
  - `/home/eze/omar-codex/docker-entrypoint.sh`
- Se buildeo la imagen de app:
  - `hhcc_app:latest`
- Se commiteo la DB actual a imagen:
  - `nuevo_cardioprieto:latest`
- Se exportaron artefactos para deploy en `/home/eze/omar`:
  - `/home/eze/omar/hhcc_app_latest.tar.gz`
  - `/home/eze/omar/nuevo_cardioprieto_latest.tar.gz`

## Verificaciones realizadas
- Sandbox MySQL `3310`: `migrate` completo OK desde cero con las migraciones actuales.
- Contenedor temporal de app contra DB real: migra sin pendientes y responde `HTTP 200`.

## Estado del sandbox
- No borrar por ahora.
- Contenedor sandbox activo:
  - `codex_sandbox_db`
- Puerto:
  - `3310`

## Archivos nuevos/relevantes a revisar en proxima sesion
- `/home/eze/omar-codex/hhcc/main/migrations/0004_schema_target_alignment.py`
- `/home/eze/omar-codex/docker-entrypoint.sh`
- `/home/eze/omar-codex/analisis_diferencias_db.txt`
- `/home/eze/omar-codex/RESUMEN_SESION_2026-04-14.md`

## Recomendacion operativa
- Esta sesion ya estaba muy cargada de contexto (`~188K/258K`).
- Conviene abrir una sesion nueva para bajar consumo del limite de 5h.
- En la nueva sesion, arrancar leyendo este archivo y luego solo los archivos tocados arriba.
