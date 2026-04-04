# Documentacion de Integracion (omar-codex + omar)

Fecha: 2026-04-03

## Objetivo
Unificar el sistema de trabajo ("omar-codex") con el repo local funcional ("omar") para obtener un **solo sistema** en `/home/eze/omar`, manteniendo en `/home/eze/omar-codex` los reportes, evidencia, RAG y scripts de auditoria.

## Repos y rol
- `/home/eze/omar` (rama `consolidacion`): **repo operativo**. Tiene auth-minima y QA reciente. Es el destino de integracion.
- `/home/eze/omar-codex`: **repo de investigacion** (reportes, scripts, RAG, evidencia). Tambien contiene un `hhcc` con apps extra (carotidas/ecostress/mmii) y templates duplicados.

## Resumen ejecutivo
- **Core (Pacientes + HC + Indicaciones)**: funcional y documentado.
- **Auth-minima**: solo esta en `/home/eze/omar`.
- **Ordenes/Solicitudes**: en `omar-codex` existen **dos flujos** (`ordenes_medicas` y `ordenes_pedicas`). En `/home/eze/omar` se dejo **uno solo** (`ordenes_medicas`), renombrado visualmente a **Solicitudes** y con PDF via `generar_pdf_orden`.
- **Templates duplicados**: en `omar-codex` hay `old_templates/` y `new_templates/` con copias. En `/home/eze/omar` ya estan archivados bajo `_archive_templates/`.
- **Apps de estudios**: `omar-codex` trae `carotidas`, `ecostress`, `mmii`; `omar` trae `earthbox` (y `ecocardiograma`). Integracion de estudios sigue pendiente.

## Estado de idempotencia y reglas
- **Idempotencia UI** se valida solo por UI y con **ID 7544**.
- Local es idempotente en comentario/visita en segunda pasada; legacy duplica (esperado).
- Regla funcional: **una visita por dia**. Si hay dos el mismo dia, editar la primera.
- Comentarios: precision **a nivel dia** (no hora). Fix aplicado en `guardar_historia` con rango UTC.

## Diferencias relevantes de codigo (hhcc)

### 1) Auth y rutas (main/urls.py)
- `/home/eze/omar`:
  - `login`, `logout`, `cambiar_nombre`, `password_change`, `password_change_done`.
  - Todas las vistas core bajo `login_required`.
- `/home/eze/omar-codex`:
  - No tiene auth ni `login_required` en rutas.

### 2) Vistas (main/views.py)
- `/home/eze/omar` incluye:
  - `logout_view`, `cambiar_nombre`.
  - `generar_pdf_orden` (WeasyPrint) con logica para `otros`.
- `/home/eze/omar-codex` incluye:
  - `ordenes_pedicas` (pantalla extra) y menu con doble entrada.
  - `detalle_paciente` existe solo en codex (redirige al detalle HC). En `omar` no esta expuesto en urls.
  - `utils.static_file_url` existe en codex, no en omar.

### 3) Templates
- Header:
  - `omar`: nombre de usuario dinamico, logo link a mini perfil, logout por link, menu unificado a **Solicitudes**.
  - `omar-codex`: usuario fijo, logout con button, menu doble (ordenes_medicas + ordenes_pedicas).
- `base.html`:
  - `omar`: incluye header solo si el usuario esta autenticado. Alpine/Tailwind por CDN.
  - `omar-codex`: Alpine/Tailwind local; siempre incluye header.
- `detalle_historia_con_historial_2.html`:
  - `omar`: boton renombrado a **Solicitudes**.
- `ordenes_medicas.html`:
  - `omar`: titulo "Solicitudes" y PDF via `generar_pdf_orden`.
  - `omar-codex`: usa `descargarPDFSolicitudes`.
- `O_M.html` (template PDF):
  - `omar`: layout ajustado y limpio.
  - `omar-codex`: version vieja.

### 4) Settings (hhcc/settings.py)
- `omar-codex`:
  - `ALLOWED_HOSTS` permisivo (`*`) via env.
  - `CSRF` deshabilitado por defecto si `DISABLE_CSRF=1` (default).
  - `INSTALLED_APPS`: `ecocardiograma`, `carotidas`, `ecostress`, `mmii`.
  - `AUTH_PASSWORD_VALIDATORS` activos (default Django).
  - `whitenoise` incluido.
- `omar`:
  - `ALLOWED_HOSTS` vacio.
  - `CSRF` activo (no removido).
  - `INSTALLED_APPS`: `ecocardiograma`, `earthbox`.
  - `AUTH_PASSWORD_VALIDATORS` vacio (relajado).
  - `LOGIN_URL/REDIRECT` configurados.

### 5) URL globales (hhcc/urls.py)
- `omar-codex`: incluye `carotidas`, `ecostress`, `mmii`.
- `omar`: incluye `earthbox`.

## Brechas funcionales detectadas (de reportes)
- Falta en local: **configuracion de usuario** (legacy tiene /usuario/configuracion/1).
- **Descarga HC** no implementada en local.
- **Comentarios eliminar**: legacy tiene endpoint dedicado; local usa endpoint JSON propio.
- **Ordenes/Solicitudes**: debe quedar **una sola** pantalla con nombre legacy: **Solicitudes**.

## Decisiones obligatorias para integracion sin dudas
1) **Canonico del flujo de Solicitudes**
   - Elegir: `ordenes_medicas` (actual en omar, usando `generar_pdf_orden`).
   - Eliminar o redirigir cualquier flujo `ordenes_pedicas`.
2) **Apps de estudios**
   - Definir si se incorporan `carotidas/ecostress/mmii` desde omar-codex al repo omar.
   - Resolver conflicto con `earthbox` y estructura de URLs.
3) **Politica de auth y password**
   - Mantener validadores vacios (actual en omar) o volver a validators de Django.
4) **CSRF y security**
   - Confirmar si se mantiene CSRF activo (omar) o se usa el toggle de codex.
5) **Templates duplicados**
   - Consolidar una sola version activa en `main/templates/`.
   - Todo lo viejo debe quedar en `_archive_templates/`.

## Estado actual de integracion (al 2026-04-03)
- Documentacion leida y consolidada.
- Diferencias de codigo identificadas.
- Listo para integrar cuando se definan los puntos de decision anteriores.

## Plan tecnico recomendado (orden)
1) **Congelar canonico**
   - Mantener `detalle_historia_con_historial_2.html` como plantilla unica de HC.
   - Borrar/archivar `detalle_historia_con_historial.html` en repos activos.
2) **Unificar Solicitudes**
   - Dejar solo `ordenes_medicas` (con `generar_pdf_orden`).
   - En menu y botones, nombre visible: **Solicitudes**.
3) **Integrar apps de estudios**
   - Migrar apps faltantes desde `omar-codex` a `omar` (si se decide).
   - Ajustar `INSTALLED_APPS` y `hhcc/urls.py`.
4) **Limpiar duplicados de templates**
   - Mover `old_templates` y `new_templates` a `_archive_templates` en omar-codex.
   - Verificar que solo se use `main/templates/`.
5) **Hardening auth/CSRF**
   - Definir politica final.
   - Ajustar settings y revisar endpoints JSON que requieren `csrf_exempt`.
6) **QA core**
   - Reejecutar checklist (Pacientes + Historias + HC + Indicaciones + Solicitudes).
   - Idempotencia solo con ID 7544.

## Archivos clave (referencias rapidas)
- `hhcc/main/views.py`
- `hhcc/main/urls.py`
- `hhcc/main/templates/components/header.html`
- `hhcc/main/templates/detalle_historia_con_historial_2.html`
- `hhcc/main/templates/ordenes_medicas.html`
- `hhcc/main/templates/O_M.html`
- `hhcc/hhcc/settings.py`
- Reportes en `Scrap_cardioprietohc/data/reports/`

## Confirmacion para integrar sin dudas
Quedo en posicion de integrar **cuando se confirmen**:
- Canonico de Solicitudes (mantener `ordenes_medicas` y eliminar `ordenes_pedicas`).
- Que apps de estudios se incluyen (carotidas/ecostress/mmii vs earthbox).
- Politica final de password y CSRF.


## Aclaraciones obligatorias (2026-04-03)
1) **Unificacion con predominio omar-codex**
   - `omar` y `omar-codex` se funden en **una sola aplicacion**.
   - El resultado final debe seguir el **enfoque tecnologico y grafico de omar-codex**.
   - **Toda decision** que implique elegir enfoque de un repo u otro **debe consultarse** antes de ejecutar.

2) **Base de datos y esquema**
   - `omar-codex` debe migrarse al **esquema MySQL de omar**.
   - Base: `cardioprieto` y configuracion de DB de `/home/eze/omar/hhcc/hhcc/settings.py`.

3) **Seguridad y validadores**
   - Mantener **validadores de password vacios**.
   - Mantener `DISABLE_CSRF=1` para pruebas (temporal).
   - Queda pendiente migrar a esquema seguro cuando se defina.

## Decision abierta: estrategia de integracion
- Pendiente definir si la integracion se realiza **directamente en `/home/eze/omar`** (release) o en una **tercera carpeta** intermedia.
- Si se crea carpeta intermedia, debe quedar claro el flujo de promotion hacia `/home/eze/omar`.

## Decision confirmada (2026-04-03)
- **Release en `/home/eze/omar`**.
- **Estilo/tecnologia predominante**: `omar-codex`.
- Toda decision de enfoque entre repos **debe ser consultada** antes de ejecutar.

## Regla visual obligatoria (2026-04-03)
- **Debe existir un solo enfoque visual**.
- El enfoque **predominante y definitivo** es `omar-codex`.
- Cualquier desviacion o mezcla debe ser consultada antes de ejecutar.

## Regla de QA post-integracion (2026-04-03)
- Despues de integrar, se ejecuta **prueba completa** y se corrigen desfasajes.

## Cambio de reglas global (2026-04-03)
- **Estilos**: usar los estilos de `/home/eze/omar`.
- **Logica de estudios**: usar la de `omar-codex`.
- **Logica NO estudios**: usar la de `omar`.
- Se reinicio el branch `integracion` al estado inicial del proceso.

## Integracion estudios (avance)
- Se sincronizaron apps desde `omar-codex` hacia `/home/eze/omar/hhcc`:
  - `ecocardiograma`
  - `carotidas`
  - `ecostress`
  - `mmii`
- Backup previo en: `/home/eze/omar/hhcc/_archive_pre_integracion_20260403/ecocardiograma_omar/`

## Plan futuro: normalizacion de migraciones
- Objetivo: consolidar migraciones una vez estabilizada la integracion.
- Pasos sugeridos:
  1) Congelar estado actual (migraciones aplicadas).
  2) Snapshot del esquema MySQL.
  3) Squash/baseline por app.
  4) Reaplicar o documentar baseline como migracion inicial consolidada.

## Migracion de datos de estudios (script)
- Script: `/home/eze/omar/scripts_migraciones/migrate_estudios_3308_to_3307.py`
- Origen: MySQL 3308, DB `cardioprieto` (solo estudios).
- Destino: MySQL 3307, DB `cardioprieto` (solo estudios).
- Tablas: `carotidas`, `stress`, `doppler -> mmii`, `ecocardiograma + eco_*`.
- Estrategia: `REPLACE` por PK, fechas de estudio con `date.today()` cuando faltan.
- Nota: el script aplica **clamp** para `peso` (<=999.99), `talla` (<=9.99) y campos decimales de eco para evitar overflow.

## Verificacion CDN vs Local (2026-04-04)
- Base CDN (legacy): `https://cardioprietohc.com/index.php/...`
- Base local (release): `http://127.0.0.1:8080/...`
- Metodo: Playwright conectado a Chromium (`--remote-debugging-port=9992`) y extraccion de valores de `input/textarea/select`.
- URLs comparadas (IDs vigentes del DB 3307):
  - Eco: CDN `https://cardioprietohc.com/index.php/eco/verEstudio/12624/11549` vs Local `http://127.0.0.1:8080/ecocardiograma/11549/?action=recuperar&estudio=12624`
  - Stress: CDN `https://cardioprietohc.com/index.php/stress/verEstudio/107/404` vs Local `http://127.0.0.1:8080/ecostress/404/?action=recuperar&estudio=107`
  - Carotidas: CDN `https://cardioprietohc.com/index.php/carotidas/verEstudio/3970/11563` vs Local `http://127.0.0.1:8080/carotidas/11563/?action=recuperar&estudio=3970`
  - MMII: CDN `https://cardioprietohc.com/index.php/doppler/verEstudio/67/11457` vs Local `http://127.0.0.1:8080/mmii/11457/?action=recuperar&estudio=67`
- Resultado:
  - Eco: campos comunes coinciden (sin diferencias de valor).
  - Carotidas: campos comunes coinciden.
  - MMII: campos comunes coinciden.
  - Stress: coincide todo salvo **whitespace** al final de `conclusion` en CDN (tabs finales). Local queda limpio.
- Nota: los contadores de campos difieren porque la UI nueva (Django) usa estructura distinta al legacy, pero los **valores comparables** coinciden.

## Verificacion PDFs (CDN vs Local) (2026-04-04)
- Metodo: Playwright + CDP para reutilizar sesion CDN, descarga de PDF y `pdftotext` para comparar texto.
- URLs de PDF (CDN):
  - Eco: `https://cardioprietohc.com/index.php/eco/imprimirEstudio/12624/11549`
  - Stress: `https://cardioprietohc.com/index.php/stress/imprimirEstudio/107/404`
  - Carotidas: `https://cardioprietohc.com/index.php/carotidas/imprimirEstudio/3970/11563`
  - MMII: `https://cardioprietohc.com/index.php/doppler/imprimirEstudio/67/11457`
- URLs de PDF (Local):
  - Eco: `http://127.0.0.1:8080/ecocardiograma/imprimir_estudio/12624/?firma=1`
  - Stress: `http://127.0.0.1:8080/ecostress/imprimir_estudio/107/404/`
  - Carotidas: `http://127.0.0.1:8080/carotidas/imprimir_estudio/3970/11563/`
  - MMII: `http://127.0.0.1:8080/mmii/imprimir_estudio/67/11457/`
- Resultado (similitud de texto):
  - Eco: ~0.71 (contenido comparable, diferencias de layout/orden).
  - Stress: ~0.86 (coincide casi completo).
  - MMII: ~0.95 (coincide casi completo).
  - **Carotidas: ~0.39 (diferencia importante)**.
- Hallazgo carotidas:
  - CDN muestra frases descriptivas (“Presenta incremento…”, “Se observa lesión…”, etc).
  - Local muestra **valores codificados** (ej: `1,2,5,8`), sugiere que el PDF no esta traduciendo codigos a texto.
  - Requiere revisar mapping en `carotidas/imprimir_estudio.html` o en helpers `com_der_texto/com_izq_texto` para que rendericen texto equivalente al legacy.
  - Fix aplicado: decodificacion de códigos en `hhcc/carotidas/models.py` + uso en `hhcc/carotidas/views.py` (PDF).
  - Resultado post-fix (ID 3970/11563): similitud sube ~0.78 y el texto coincide semánticamente.

## Pendientes opcionales (para futura conversacion)
- Afinar PDF de ecocardiograma (layout/orden).
- Alinear labels PDF de stress (solo estetica/orden, contenido OK).
- Revisión visual general post-integracion.

## Resumen final (estado actual)
- Integracion base en `/home/eze/omar` con apps de estudios incorporadas desde `omar-codex`.
- Migracion de datos de estudios aplicada (3308 -> 3307), con limpieza de `<br>` en texto.
- Comparacion CDN vs local OK en datos; PDF de carotidas corregido para mostrar texto descriptivo.
- UI ecocardiograma: interlineado y altura de combos ajustados.
- UI ecostress: removida normalizacion que rompia JS (datos cargan OK).
- Lista de estudios por historia (nuevo):
  - Nueva vista `/historias/<id>/estudios/` con filtro por fecha y acciones Ver/Imprimir/Enviar (placeholder).
  - Link desde listado de historias en el icono de estudios.
  - Iconos en la tabla (ver/imprimir/enviar).
- Paginador actualizado en historias y pacientes (estilo omar-codex).
- Estilos recuperados de omar-codex:
  - Títulos `h1/h2/h3` centrados.
  - Breadcrumbs / current-path.

## Fix aplicado: UI tolerante ecostress (2026-04-04)
- Se elimino normalizacion `<br>` en ecostress porque introducia **SyntaxError** en JS inline.
- Error original: `Unexpected token '>'` por regex `/...\/?>/` dentro de `<script>` sin escape, lo que anulaba Alpine (`ecostressForm is not defined`) y dejaba campos vacios.
- Cambio: remover `normalizeText()` y sus usos en `hhcc/ecostress/templates/ecostress/nuevo_estudio.html`.
- Resultado: Alpine inicializa y se llenan datos correctamente.

## Fix aplicado: UI tolerante ecocardiograma (2026-04-04)
- Se revirtio `normalizeText()` en `hhcc/ecocardiograma/templates/ecocardiograma/eco_form.html` a pedido (DB ya no tiene `<br>`).

## Nota operativa (recuperar estudio especifico)
- Para forzar estudio puntual: `?action=recuperar&estudio=<id>`.
