# CONTEXTO (general)

## Ubicaciones clave
- Sandbox de trabajo: `/home/eze/omar-codex`.
- Proyecto Django (sandbox editable): `/home/eze/omar-codex/hhcc` (apps: `main`, `ecocardiograma`, `carotidas`, `ecostress`, `doppler`).
- Proyecto Django “oficial” (solo lectura): `/home/eze/omar/hhcc`.
- Scraper completo del sitio original: `/home/eze/omar-codex/Scrap_cardioprietohc`.
- Dumps locales del server nuevo: `/home/eze/omar/scrap_local_8080/data/raw/`.

## Sistemas
- Sitio viejo: `https://cardioprietohc.com`.
  - Credenciales: usuario `omar`, password `Corbis5`.
  - Endpoints relevantes (legacy): login, pacientes, historias, carótidas.
- Sitio nuevo: `http://localhost:8080` (sin auth, en el entorno local).

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
- URLs: raíz -> `main`, `/ecocardiograma/`, `/carotidas/`, `/ecostress/`, `/doppler/`.
- Se mantiene Tailwind/Alpine pero se busca replicar flujos del legacy.
- Pendiente general: ajustar pacientes a `numDoc`, sexo `H/M`, eliminar, AJAX, validaciones, feedbacks.

## DB y entorno
- `hhcc/hhcc/settings.py`: DB default MySQL (localhost 127.0.0.1:3307).
- Flag `USE_SANDBOX_DB=1` fuerza sqlite (`db.sqlite3`) para pruebas en sandbox.

## Cómo correr en sandbox
```bash
cd /home/eze/omar-codex/hhcc
USE_SANDBOX_DB=1 python manage.py runserver 0.0.0.0:8090
```

## URLs de prueba (sandbox)
- Carótidas: `http://localhost:8090/carotidas/1/nuevo/`
- Ecostress: `http://localhost:8090/ecostress/1/nuevo/`
- Doppler MMII arterial: `http://localhost:8090/doppler/1/nuevo/`

## Impresión (global)
- Base común de impresión: `hhcc/main/templates/print_base.html`.
- CSS común: `hhcc/main/static/main/css/print.css` (cargado vía `file:///`).
- Base parametrizable: `print_logo_path`, `print_site_text`, `print_header_text`.

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
- Se implementó la app `doppler` en Django (modelo, form, vistas, templates y migración inicial).


- Se creó venv RAG en `Scrap_cardioprietohc/.venv_rag` con dependencias para reindexar.
- RAG reindexado: `data/cache/rag_index.pkl`.

- El índice RAG es único: `Scrap_cardioprietohc/data/cache/rag_index.pkl`. El venv solo sirve para reindexar, no crea catálogos separados.
