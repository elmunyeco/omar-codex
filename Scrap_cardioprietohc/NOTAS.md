# Notas consolidadas (Scrap_cardioprietohc)

## Pautas clave
- Visualización prioritaria: reproducir layout/posiciones/colores/espaciados/componentes del sistema original; no cambiar UI salvo pedido explícito o mejora indiscutible.
- Si faltan assets, obtenerlos antes de tocar plantillas.
- No borrar ni mover archivos en `data/raw` sin aprobación; preservar HTML/JSON del scrape.

## Configuración scraper
- `.env`: BASE_URL (default https://cardioprietohc.com/), LOGIN_PATH (/index.php/login/validarUsuario), PACIENTES_PATH (/index.php/pacientes/index), HISTORIAS_PATH (/index.php/historias/index), USERNAME/PASSWORD, OUTPUT_DIR=data/raw.
- client.py: urljoin, postea `usuario`/`pass`; si LOGIN_PATH vacío, acceso público.
- crawlers: pacientes pagina hasta 3, guarda HTML numerado y assets; historias usa HISTORIAS_PATH y descarga assets.
- pipelines: guarda JSON/HTML y assets en `data/raw/assets` sin borrar existentes.

## Datos scrapeados
- HTML/JSON: pacientes_list_1/2/3.html, pacientes_add.html, pacientes_edit_dni12.html, pacientes_search_dni12.html, pacientes.json, funciones.js (cache).
- Assets: `data/raw/assets/` (css/js/img).
- Headless: screenshots y HTML renderizado (páginas, búsqueda, alta sin enviar, edición) en `data/raw/screenshots*/` y `data/raw/rendered*`.
- Índice RAG: `data/cache/rag_index.pkl` (generado sobre todo `data/raw`).

## UI/UX original (Pacientes)
- Sidebar: activo rojo #D9100C, fondo rgba(217,16,12,0.5), borde izq 5px, texto blanco.
- Buscador: POST `/index.php/pacientes/buscador`, padding-left 40/padding-top 10, input width 40%, botón alta derecha (padding-right 150, icono plus).
- Tabla: cols #/Nombre/Apellido/Editar/Eliminar; filas `.fila_<id>`, glyphicons; paginador en páginas 2/3.
- Formularios: form-horizontal (label col-4 + input col-4) apilado; campos tipoDoc, numDoc, nombre, apellido, fechaNac (cálculo edad), sexo H/M, email, dirección, localidad, obraSocial, plan, afiliado, teléfono, celular, profesión, referente; mensajes éxito/error y acciones post-alta (ocultas).
- JS: `funciones.js` con AJAX de alta/edición, buscador (reemplaza tbody y oculta paginador), eliminar fila, validación fecha/edad.
- Colores: #D9100C, #d9534f, #428bca/#357ebd, #eee, blanco. Tipografía Bootstrap default; iconos FontAwesome+Glyphicons.

## Cómo levantar
- Sandbox/restringido: `codex --workspace /home/eze/culo/Scrap_cardioprietohc --sandbox-mode workspace-write --network-access restricted` y trabajar con data local; regenerar índice si hace falta.
- Con red: `codex --workspace /home/eze/culo/Scrap_cardioprietohc --sandbox-mode workspace-write --network-access enabled`; luego `source .venv/bin/activate`, `python -m scrap_cardioprietohc.cli run --target pacientes`, `python -m scrap_cardioprietohc.cli rag-index --source data/raw --index data/cache/rag_index.pkl`.
- Headless local: `python scrap_cardioprietohc/headless_capture.py` (sitio original) o `headless_capture_local.py` (localhost:8080, con ajustes de BASE_URL si aplica).

## TODO / Issues (Pacientes Django vs scrape)
- Campos: usar `numDoc` en lista; sexo `H/M` (no `M/F`).
- Flujos: añadir eliminar en lista y feedback (buscar/errores), decidir GET vs POST/AJAX como original; considerar ocultar paginador en búsqueda.
- Validaciones/UX: portar lo útil de `funciones.js` a Alpine/fetch (mensajes, reemplazo tbody, cálculo edad, estados post-alta).
- Estilo: alinear sidebar/buscador/tabla/botones al layout original manteniendo Tailwind/Alpine; paleta acotada y consistencia.
- Migrar scraper al repo Django (si aplica) sin `.venv` y recrear índice; actualizar rutas en notas.
