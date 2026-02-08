# Resumen operativo (Pacientes) - Scrap_cardioprietohc

## 1) Configuración actual
- Base: `https://cardioprietohc.com/`
- Paths: login `/index.php/login/validarUsuario`, pacientes `/index.php/pacientes/index`, historias `/index.php/historias/index`
- Credenciales (en `.env`): usuario `omar`, pass `Corbis5` (no subir a git)
- Código: `client.py` (login usuario/pass), `crawlers` (paginan, guardan HTML+assets sin borrar), `pipelines` (assets a `data/raw/assets`), `headless_capture.py` (Playwright).

## 2) Datos descargados
- Listados: `data/raw/pacientes_list_1/2/3.html` + assets en `data/raw/assets/`.
- Formularios: `pacientes_add.html`, `pacientes_edit_dni12.html`, `pacientes_search_dni12.html`, `pacientes.json`, `funciones.js` (en `data/cache`).
- Capturas headless: `data/raw/screenshots/nav_*.png` (login, páginas 1/2/3, búsqueda DNI 12 before/after, alta sin enviar, edición Pirulin).
- HTML renderizado Playwright: `data/raw/rendered/pacientes_page_1/2/3.html`.
- Índice RAG: `data/cache/rag_index.pkl` (indexa todo `data/raw`).

## 3) UI/UX Pacientes (lo que hay que clonar)
- Sidebar: activo rojo `#D9100C`, fondo `rgba(217,16,12,0.5)`, texto blanco, borde izq 5px.
- Buscador: input + botón search + select filtro; padding-left 40, padding-top 10; botón alta a la derecha (padding-right 150, padding-top 30, icono plus 24px).
- Tabla: cols #/Nombre/Apellido/Editar/Eliminar; filas `.fila_<id>` con glyphicons lápiz/cruz; paginador en páginas 2/3.
- Form alta/edición: `form-horizontal`, grupos apilados (label col-xs-4, input col-xs-4). Campos: tipoDoc, numDoc, nombre, apellido, fechaNac (dd/mm/yyyy con cálculo edad), sexo H/M, email, dirección, localidad, obraSocial, plan, afiliado, teléfono, celular, profesión, referente. Mensajes `.msjPaciente`/`.msjError`, acciones `.btnOpcs` (ocultos por default), loader GIF.
- Colores: `#D9100C`, `#d9534f`, `#428bca/#357ebd`, `#eee`, blanco. Tipografía: Bootstrap default; iconos FontAwesome + Glyphicons.
- JS (`funciones.js`): AJAX alta/edición, buscador (reemplaza tbody y oculta paginador), eliminar filas, validación fecha/edad.

## 4) Cómo levantar Codex/scraper
- Normal (sandbox/restringido):
  ```
  codex --workspace /home/eze/culo/Scrap_cardioprietohc --sandbox-mode workspace-write --network-access restricted
  ```
  Trabajar con `data/raw` local y regenerar índices.
- Con red (para scrapear):
  ```
  codex --workspace /home/eze/culo/Scrap_cardioprietohc --sandbox-mode workspace-write --network-access enabled
  cd /home/eze/culo/Scrap_cardioprietohc
  source .venv/bin/activate
  python -m scrap_cardioprietohc.cli run --target pacientes
  python -m scrap_cardioprietohc.cli rag-index --source data/raw --index data/cache/rag_index.pkl
  ```
- Headless Playwright (capturas):
  ```
  python scrap_cardioprietohc/headless_capture.py
  ```

## 5) Pautas obligatorias
- No borrar ni mover nada en `data/raw` sin aprobación.
- Visual es prioridad: replicar layout/espaciados/colores/componentes antes de tocar lógica; no cambiar UI salvo pedido o mejora indiscutible.
- Si faltan assets, bajarlos antes de modificar plantillas.
