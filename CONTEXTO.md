# CONTEXTO (general)

## Ubicaciones clave
- Sandbox de trabajo: `/home/eze/omar-codex`.
- Proyecto Django (sandbox editable): `/home/eze/omar-codex/hhcc` (apps: `main`, `ecocardiograma`, `carotidas`).
- Proyecto Django “oficial” (solo lectura): `/home/eze/omar/hhcc`.
- Scraper completo del sitio original: `/home/eze/culo/Scrap_cardioprietohc` (copia parcial en `/home/eze/omar-codex/Scrap_cardioprietohc`).
- Dumps locales del server nuevo: `/home/eze/omar/scrap_local_8080/data/raw/`.

## Sistemas
- Sitio viejo: `https://cardioprietohc.com`.
  - Credenciales: usuario `omar`, password `Corbis5`.
  - Endpoints relevantes (legacy): login, pacientes, historias, carótidas.
- Sitio nuevo: `http://localhost:8080` (sin auth, en el entorno local).

## Scraper del sitio viejo (resumen)
- Config en `.env` de `/home/eze/culo/Scrap_cardioprietohc`:
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
- URLs: raíz -> `main`, `/ecocardiograma/`, `/carotidas/`.
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

## Próximos objetivos generales
- Completar UI/flujo de pacientes con comportamiento legacy.
- Integrar carótidas a las vistas clínicas cuando esté validado.
- Mantener simplificación visual sin perder funcionalidad.



## Impresión carótidas
- Endpoint de impresión en sandbox: `/carotidas/imprimir_estudio/<estudio_id>/<historia_id>/`.
- Template A4: `hhcc/carotidas/templates/carotidas/imprimir_estudio.html`.
- Submit de carótidas usa AJAX y abre nueva ventana con la impresión.
- PDF legacy descargado en `Scrap_cardioprietohc/data/raw/carotidas/imprimirEstudio_4512_7544.pdf`.


## Impresión carótidas (PDF)
- Impresión genera PDF via WeasyPrint y oculta secciones vacías.
- Endpoint responde `application/pdf`.

- WeasyPrint sin base_url en impresión carótidas para evitar DisallowedHost.


## i18n global
- Se fuerza idioma `es-ar` para todas las requests mediante middleware.
- Archivo: `hhcc/hhcc/middleware.py` (`force_spanish_middleware`).
- Registrado en `hhcc/hhcc/settings.py` (MIDDLEWARE).


## Template base de impresión
- Base común para informes: `hhcc/main/templates/print_base.html`.
- Los informes PDF deberían extender esta base para layout homogéneo.


## Base de impresión parametrizada
- `print_base.html` ahora acepta variables `print_logo_path`, `print_site_text`, `print_header_text`.
- Ecocardiograma y carótidas pasan estos valores desde sus vistas de impresión.
- Plantillas de impresión deben extender `print_base.html` para homogeneidad.

- Se creó `ECOCARDIOGRAMA.md` con el estado de impresión del módulo.


- CSS común de impresión: `hhcc/main/static/main/css/print.css` (usado por print_base).


## Copia de /home/eze/culo
- Se copió el scraper completo a `/home/eze/omar-codex/Scrap_cardioprietohc` (incluye data, assets, RAG, notas).
- Se copiaron referencias: `RESUMEN_PARA_MI.md`, `TODO_culo.md`.
- Se copiaron esquemas SQL: `esquema_nuevo_cardioprieto_2025-12-07.sql`, `esquema_viejo_cardioprieto_2025-12-07.sql`.
