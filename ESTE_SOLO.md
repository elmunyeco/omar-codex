# TODO/CONTEXTO ÚNICO (usar este archivo)

## Workspaces y ubicaciones
- Proyecto Django nuevo: `/home/eze/omar-codex/hhcc` (apps: main, ecocardiograma, carotidas).
- Scraper completo (sitio original): `/home/eze/culo/Scrap_cardioprietohc` (con datos, assets, RAG, headless, notas). En omar-codex también hay una copia parcial en `Scrap_cardioprietohc` pero la “buena” es la de `culo`.
- Resumen rápido de carótidas: `/home/eze/omar-codex/RESUMEN_CAROTIDAS.md` (duplicado aquí).
- Resúmenes/TODO previos: `/home/eze/culo/RESUMEN_PARA_MI.md`, `/home/eze/culo/TODO.md`, `/home/eze/omar-codex/Scrap_cardioprietohc/NOTAS.md`.

## Scraper (sitio original)
- Config (en `.env` de `/home/eze/culo/Scrap_cardioprietohc`): `BASE_URL=https://cardioprietohc.com/`, `LOGIN_PATH=/index.php/login/validarUsuario`, `PACIENTES_PATH=/index.php/pacientes/index`, `HISTORIAS_PATH=/index.php/historias/index`, credenciales omar/Corbis5, `OUTPUT_DIR=data/raw`.
- Código: `client.py` (login usuario/pass), `crawlers` (pacientes/historias, paginan hasta 3, guardan HTML y assets sin borrar), `pipelines` (assets a `data/raw/assets`), `headless_capture.py` (original; falla en este entorno por sandbox).
- Datos: `data/raw/pacientes_list_1/2/3.html`, `pacientes_add.html`, `pacientes_edit_dni12.html`, `pacientes_search_dni12.html`, `pacientes.json`, `funciones.js` (en data/cache). Assets en `data/raw/assets/` (css/js/img). Screenshots/headless y HTML renderizado (en la copia buena de `culo`: `data/raw/screenshots*`, `data/raw/rendered*`).
- Índice RAG: `data/cache/rag_index.pkl` (regenerar con `python -m scrap_cardioprietohc.cli rag-index --source data/raw --index data/cache/rag_index.pkl`).
- Paleta/UX original (pacientes): sidebar activo rojo `#D9100C` con fondo rgba(217,16,12,0.5), borde izq 5px; buscador con padding-left 40/top 10, input width 40%, botón alta derecha (padding-right 150, icono plus); tabla cols #/Nombre/Apellido/Editar/Eliminar, filas `.fila_<id>` con glyphicons; paginador en páginas 2/3; form-horizontal (label col-4 + input col-4) apilado; campos tipoDoc, numDoc, nombre, apellido, fechaNac (cálculo edad), sexo H/M, email, dirección, localidad, obraSocial, plan, afiliado, teléfono, celular, profesión, referente; mensajes éxito/error, acciones post-alta ocultas. JS `funciones.js`: AJAX alta/edición, buscador (reemplaza tbody y oculta paginador), eliminar fila, validación fecha/edad.
- Headless en este entorno suele fallar por sandbox (`FATAL: ... shutdown: Operation not permitted`). Usar curl/requests o ejecutar headless en tu host.

## Módulo Carótidas (sitio original)
- HTML autenticado: `Scrap_cardioprietohc/data/raw/carotidas/carotidas_7544_authed.html` (login omar/Corbis5). Assets en `data/raw/carotidas/assets/` (bootstrap.css, font-awesome.min.css, carotidas.css, jquery.min.js, carotidas.js, logo/iconos).
- Tabla legacy `carotidas`: id, idHC, comDerecha/intDerecha/extDerecha/comIzquierda/intIzquierda/extIzquierda, artVertebrales, sugerencias, idComDer/idComIzq, espIntMedDer/Izq (decimal 4,2).
- Formulario `#formCarotidas`:
  - Hidden: idHC, idEstudio, idComDer, idComIzq.
  - Por arteria: select (carótida común Der/Izq) con opción “otras” + comentario; radios carótida interna/externa Der/Izq con sub-radios (estabilidad, localización, estenosis); espesor íntima-media Der/Izq (validación numérica); vertebrales y sugerencias (radios). Botón clear por bloque.
  - Pre-informe: spans `.orden_*` se actualizan según selecciones/comentarios; triggers iniciales.
  - Validación numérica: solo dígitos/punto/coma; regex `^\d{1,2}$|^\d{1,2}\.\d{1,2}$`; alerta y limpia si inválido.
  - Submit: AJAX POST serialize a `/carotidas/guardarInforme`; si éxito, setea idEstudio, abre `imprimirEstudio/{id}/{idHC}`, re-habilita botones; errores muestran mensaje. No enviar estudios en análisis.
  - Layout: bootstrap clásico, panel datos paciente, títulos QIMT, boxes con selects/radios/comentarios, pre-informe a la derecha.

## Django nuevo (hhcc) - estado
- Apps en `INSTALLED_APPS`: main, ecocardiograma, carotidas.
- URLs: raíz -> main; `/ecocardiograma/` y `/carotidas/`.
- App `carotidas` (nueva):
  - Modelo `CarotidasEstudio` (alineado a tabla legacy): FK `historia` (HistoriaClinica), campos com/int/ext Der/Izq, art_vertebrales, sugerencias, id_com_der/izq, esp_int_med_der/izq (decimal 4,2). Índices en historia y id_com_der/id_com_izq.
  - Form `CarotidasForm`: campos del modelo, historia oculto; normaliza coma->punto en decimales.
  - Vistas: `nuevo_estudio(historia_id)` (crea/edita primer estudio de esa HC) y `detalle_estudio(pk)` (placeholder). Usa `carotidas/nuevo_estudio.html` y `carotidas/detalle_estudio.html` (a crear).
  - URLs: `/<historia_id>/nuevo/`, `/estudio/<pk>/`.
  - Admin: `CarotidasEstudioAdmin` listado básico.
  - Templates pendientes; migraciones pendientes (correr `python manage.py makemigrations carotidas && python manage.py migrate`).
- App main (pacientes) vs. scrape:
  - Lista usa `paciente.dni` (debería `numDoc`), solo acción editar, búsqueda GET, sin eliminar ni AJAX; estilos tailwind (#9a4035) no coinciden con UI original.
  - Formularios usan sexo `M/F` (modelo es `H/M`), layout grid tailwind, sin mensajes/loader ni flujo AJAX.
  - Falta acción eliminar en lista; paginación estándar.

## Objetivos/decisiones UX
- Mantener Tailwind/Alpine (mejor que Bootstrap/jQuery), pero recuperar flujos/acciones del original: numDoc correcto, sexo H/M, eliminar en lista, feedback/mensajes, búsqueda con reset, validaciones clave (fecha/edad, numéricos).
- Paleta acotada, menos distracción/menús, foco en tareas; patrones de navegación/feedback consistentes.
- Para carótidas: portar lógica/validaciones a Tailwind/Alpine sin romper DB; definir estilo propio respetando estructura de informe y pre-informe/imprimir.

## Cómo levantar Codex / scraper
- Modo restringido (sin red): `codex --workspace /home/eze/culo/Scrap_cardioprietohc --sandbox-mode workspace-write --network-access restricted`; trabajar con data local y regenerar índice.
- Con red (scrapear): `codex --workspace /home/eze/culo/Scrap_cardioprietohc --sandbox-mode workspace-write --network-access enabled`; luego `source .venv/bin/activate` y comandos de run/index.
- Headless: scripts `headless_capture.py` (sitio original, puede fallar por sandbox aquí) y `headless_capture_local.py` (ajustar BASE_URL para localhost; en este entorno falló el sandbox).

## Tareas pendientes (prioridad)
- Generar migraciones para `carotidas` y crear templates (`carotidas/nuevo_estudio.html`, `detalle_estudio.html`) basados en lo scrapeado.
- Decidir ajustes en pacientes (lista/form) respecto a los flujos originales y corregir `numDoc`/sexo.
- Si se mueve el scraper al repo Django: copiar sin `.venv`, recrear venv/Playwright y reindexar; actualizar rutas en notas.
- Reindexar RAG tras agregar carótidas si se modifica `data/raw` en este workspace: `python -m scrap_cardioprietohc.cli rag-index --source data/raw --index data/cache/rag_index.pkl`.
