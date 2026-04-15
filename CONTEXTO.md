# CONTEXTO (general)

## Ubicaciones clave
- Asociación permanente de trabajo: `/home/eze/omar-codex` y `/home/eze/omar` se tratan como dos repositorios de un mismo negocio y deben considerarse juntos en cualquier análisis/cambio.
- Sandbox de trabajo: `/home/eze/omar-codex`.
- Proyecto Django (sandbox editable): `/home/eze/omar-codex/hhcc` (apps: `main`, `ecocardiograma`, `carotidas`, `ecostress`, `mmii`).
- Proyecto Django “oficial” (solo lectura): `/home/eze/omar/hhcc`.
- Directorio legacy/base del sistema (solo lectura): `/home/eze/omar` (DB MySQL).
- Scraper completo del sitio original: `/home/eze/omar-codex/Scrap_cardioprietohc`.
- Dumps locales del server nuevo: `/home/eze/omar/scrap_local_8080/data/raw/`.
- Scrape base (solo GET, sistema `/home/eze/omar`): `/home/eze/omar-codex/scrap_local_8080_base`.

## Sistemas
- Sitio viejo: `https://cardioprietohc.com`.
  - Credenciales: usuario `omar`, password `Corbis5`.
  - Endpoints relevantes (legacy): login, pacientes, historias, carótidas.
- Sitio nuevo: `http://localhost:8080` (sin auth, en el entorno local).
- Sistema base (legacy Django): `http://127.0.0.1:8080` (solo lectura; integración pendiente).
- Regla de integración: ante discrepancias en estilos, templates o arquitectura compartida,
  **prevalece `/home/eze/omar-codex`** (versión más nueva).
- Regla de reemplazo de estudios: todo lo de **carótidas, doppler/MMII y stress/ecostress**
  en `/home/eze/omar` o en MySQL se reemplaza por lo ya implementado en `/home/eze/omar-codex`.
  Además, **ecocardiograma** se incorpora desde `/home/eze/omar-codex`.
- Regla UI global: **los breadcrumbs desaparecen de todo el sistema**.

## Scraper del sitio viejo (resumen)
- Config en `.env` de `Scrap_cardioprietohc`:
  - `BASE_URL=https://cardioprietohc.com/`
  - `LOGIN_PATH=/index.php/login/validarUsuario`
  - `PACIENTES_PATH=/index.php/pacientes/index`
  - `HISTORIAS_PATH=/index.php/historias/index`
  - `OUTPUT_DIR=data/raw`
- Código principal: `client.py`, `crawlers`, `pipelines`, `headless_capture.py`.
- Headless suele fallar por sandbox en este entorno.
- Índice RAG: `data/cache/rag_index.pkl` (regenerar con `python -m scrap_cardioprietohc.cli rag-index --source data/raw --index data/cache/rag_index.pkl`).

## Dumps locales del server nuevo (localhost:8080)
- HTML guardado en `/home/eze/omar/scrap_local_8080/data/raw/`:
  - `pacientes_list.html`, `pacientes_edit_11564.html`, `pacientes_crear.html`
  - `historias_list.html`, `historial_medico_11564.html`
- Assets locales descargados: `static/main/css/style.css`, `js/components/header.js`, `images/logo.png`.
- Falló CDN tailwind (403); Alpine se guardó con URL sin esquema correcto.
- Scrape hecho con `curl` sin auth.

## Estado general del Django nuevo (sandbox)
- URLs: raíz -> `main`, `/ecocardiograma/`, `/carotidas/`, `/ecostress/`, `/mmii/`.
- Se mantiene Tailwind/Alpine pero se busca replicar flujos del legacy.
- Pendiente general: ajustar pacientes a `numDoc`, sexo `H/M`, eliminar, AJAX, validaciones, feedbacks.

## Static y Docker (out-of-the-box)
- Tailwind y Alpine se sirven en local (no CDN):
  - `hhcc/main/static/main/css/tailwind.min.css`
  - `hhcc/main/static/main/js/alpine.min.js`
- `whitenoise` habilitado para servir estáticos en gunicorn.
- `STATIC_ROOT=/app/hhcc/staticfiles` con `collectstatic` en build Docker.
- Dockerfile exporta `DJANGO_ALLOWED_HOSTS=*` para evitar `DisallowedHost` en test.
- CSRF desactivado por default en entorno de prueba (`DISABLE_CSRF=1`).

## DB y entorno
- `hhcc/hhcc/settings.py`: DB default MySQL (localhost 127.0.0.1:3307).
- Flag `USE_SANDBOX_DB=1` fuerza sqlite (`db.sqlite3`) para pruebas en sandbox.

## Cómo correr en sandbox
```bash
cd /home/eze/omar-codex/hhcc
USE_SANDBOX_DB=1 python manage.py runserver 0.0.0.0:8090
```

## Nota DB
- Si corrés con `USE_SANDBOX_DB=1`, también migrar con ese flag para evitar warnings.

## URLs de prueba (sandbox)
- Carótidas: `http://localhost:8090/carotidas/1/`
- Ecostress: `http://localhost:8090/ecostress/1/`
- MMII arterial: `http://localhost:8090/mmii/1/`

## Impresión (global)
- Base común de impresión: `hhcc/main/templates/print_base.html`.
- CSS común: `hhcc/main/static/main/css/print.css` (cargado vía `file:///`).
- Base parametrizable: `print_logo_path`, `print_site_text`, `print_header_text`.
- Logo de membretes actualizado: `logo_omar_prieto.svg` (fallback a `logo.png` vía `onerror` en headers y `print_base.html`).
- Tamaño de logo en PDF: `.logo { height: 48px; max-width: 270px; object-fit: contain; }`.
 - Header PDF: logo a la izquierda y datos (Nombre/Fecha/HC) a la derecha, repetidos en todas las páginas (WeasyPrint `@page` + `position: running(page-header)`).
 - Layout del header: `table` 40% logo / 60% datos; alineación derecha en datos.
 - Línea de separación: solo borde inferior del header (`border-bottom: 1px solid #e5e7eb`).
 - Margen superior de página para header: `@page margin-top: 50mm`.
- Títulos en PDF centrados y sin subrayado (estilos globales en `print.css`).

## Títulos y textos libres (UI)
- Títulos (`h1/h2/h3`) centrados y sin subrayado (estilos globales en `style.css`).
- Contador de caracteres solo para campos con `maxlength > 512` (JS común `main/static/main/js/char_counter.js`).
- Límites: comentarios generales `512`, conclusiones `8000`.
- Bloque de acciones (Firmar PDF + Guardar + Volver) centrado en todos los estudios.
- Mensajes de guardado: éxito en verde, error en rojo; el error se auto‑cierra a los 15s, el éxito no.
 
## Firma PDF (opcional)
- Todos los PDFs soportan firma opcional con `?firma=1`.
- Firma visible: “Dr. Omar Prieto” / “cardiologo” alineado a la derecha.
- Separación antes de la firma aumentada (más aire visual).

## Logos (assets)
- SVG final en raíz: `logo_omar_prieto.svg` y PNG `logo_omar_prieto.png`.
- Copiados a estáticos: `hhcc/main/static/main/images/logo_omar_prieto.svg` y `.png`.
- SVG auxiliar del isotipo: `logo_circulo_solo_stroke_corazon.svg`.

## PDFs de prueba (sandbox)
- Generados: `hhcc/ecocardiograma_1_1.pdf`, `hhcc/carotidas_1_1.pdf`, `hhcc/mmii_1_1.pdf`.
- `ecostress` no tiene tabla en `db.sqlite3` (si se necesita, generar desde app en ejecución).
 - Nuevos estudios de prueba con lorem (HC 7):
   - Ecocardiograma `id=3` (con conclusión larga).
   - Carótidas `id=7`.
   - MMII `id=3`.
   - Ecostress `id=2` (existente).
 - URLs de prueba:
   - `http://127.0.0.1:8000/ecocardiograma/imprimir_estudio/3/`
   - `http://127.0.0.1:8000/carotidas/imprimir_estudio/7/7/`
   - `http://127.0.0.1:8000/mmii/imprimir_estudio/3/7/`
   - `http://127.0.0.1:8000/ecostress/imprimir_estudio/2/7/`
 - Nuevos estudios con máximos (HC 8, sandbox 8090):
   - Ecocardiograma `id=4` (conclusión B 8000, comentario final 8000).
   - Carótidas `id=8` (comentarios 512).
   - MMII `id=5` (conclusión 8000).
   - Ecostress `id=5` (conclusión 8000).
 - URLs PDF (sandbox 8090):
   - `http://127.0.0.1:8090/ecocardiograma/imprimir_estudio/4/`
   - `http://127.0.0.1:8090/carotidas/imprimir_estudio/8/8/`
   - `http://127.0.0.1:8090/mmii/imprimir_estudio/5/8/`
   - `http://127.0.0.1:8090/ecostress/imprimir_estudio/5/8/`

## i18n global
- Se fuerza idioma `es-ar` para todas las requests mediante middleware.
- Archivo: `hhcc/hhcc/middleware.py` (`force_spanish_middleware`).
- Registrado en `hhcc/hhcc/settings.py` (MIDDLEWARE).

## Copia de /home/eze/culo
- Se copió el scraper completo a `/home/eze/omar-codex/Scrap_cardioprietohc` (incluye data, assets, RAG, notas).
- Se copiaron esquemas SQL: `esquema_nuevo_cardioprieto_2025-12-07.sql`, `esquema_viejo_cardioprieto_2025-12-07.sql`.

## Pacientes (legacy UX) - resumen operativo
- Sidebar activo rojo `#D9100C`, fondo `rgba(217,16,12,0.5)`, texto blanco, borde izq 5px.
- Buscador: input + botón search + select filtro; padding-left 40, padding-top 10; botón alta a la derecha (padding-right 150, padding-top 30, icono plus 24px).
- Tabla: cols #/Nombre/Apellido/Editar/Eliminar; filas `.fila_<id>` con glyphicons lápiz/cruz; paginador en páginas 2/3.
- Form alta/edición: `form-horizontal`, grupos apilados (label col-xs-4, input col-xs-4).
  Campos: tipoDoc, numDoc, nombre, apellido, fechaNac (dd/mm/yyyy con cálculo edad), sexo H/M, email, dirección, localidad, obraSocial, plan, afiliado, teléfono, celular, profesión, referente.
- Mensajes `.msjPaciente`/`.msjError`, acciones `.btnOpcs` (ocultos por default), loader GIF.
- Colores: `#D9100C`, `#d9534f`, `#428bca/#357ebd`, `#eee`, blanco. Tipografía Bootstrap; iconos FontAwesome + Glyphicons.
- JS (`funciones.js`): AJAX alta/edición, buscador (reemplaza tbody y oculta paginador), eliminar filas, validación fecha/edad.

## Scraper operativo (pacientes)
- Base `https://cardioprietohc.com/` y paths login/pacientes/historias.
- Credenciales en `.env` (omar/Corbis5).
- Capturas: `data/raw/screenshots/nav_*.png`; HTML renderizado `data/raw/rendered/pacientes_page_*.html`.
- Índice RAG: `data/cache/rag_index.pkl`.

- Se creó `ECOSTRESS.md` con el detalle del módulo de Ecostrés (HTML, JS, CSS, campos, flujo).
- Se creó `DOPPLER_MMII_ARTERIAL.md` con el detalle del módulo Doppler arterial de MMII (HTML, JS, CSS, campos, flujo).
- Se implementó la app `ecostress` en Django (modelo, form, vistas, templates y migración inicial).
- Se implementó la app `mmii` en Django (modelo, form, vistas, templates y migraciones de renombre desde `doppler`).
- Renombre global `doppler` → `mmii`: app, URLs `/mmii/`, templates, assets y tabla DB.
- `print_base.html` default site text: `www.cardioprieto.com`.


- Se creó venv RAG en `Scrap_cardioprietohc/.venv_rag` con dependencias para reindexar.
- RAG reindexado: `data/cache/rag_index.pkl`.

- El índice RAG es único: `Scrap_cardioprietohc/data/cache/rag_index.pkl`. El venv solo sirve para reindexar, no crea catálogos separados.
