# Notas rápidas (Scrap_cardioprietohc en omar-codex)

## Estado general
- Scrape y almacenamiento en `data/raw/` (HTML, assets descargados en `data/raw/assets/`).
- RAG se puede regenerar: `python -m scrap_cardioprietohc.cli rag-index --source data/raw --index data/cache/rag_index.pkl`.
- Playwright headless en este entorno puede fallar por sandbox; usar curl/requests para bajar HTML/JS/CSS.

## Carótidas (nuevoEstudio/7544)
- HTML autenticado guardado: `data/raw/carotidas/carotidas_7544_authed.html`.
- Assets descargados en `data/raw/carotidas/assets/`:
  - CSS: `bootstrap.css`, `font-awesome.min.css`, `carotidas.css`
  - JS: `jquery.min.js`, `carotidas.js`
  - Imágenes: `logo.jpg`, `icono.png`
- Formulario `#formCarotidas` (action `/index.php/carotidas/guardarInforme`):
  - Hidden: `idHC=7544`, `idEstudio=0`, `idComDer=0`, `idComIzq=0`.
  - Campos select + radios por arteria (carótida común/interna/externa derecha/izquierda, vertebrales, sugerencias) y comentarios; espesor íntima-media derecha/izquierda (`espIntMedDer/espIntMedIzq`) numéricos.
  - No enviar nuevos estudios: el JS envía AJAX y abre `imprimirEstudio/{id}/{idHC}`; acá solo análisis.
- JS (`carotidas.js`) comportamiento:
  - `.btnSubmit` dispara submit; submit via AJAX POST serialize form; si `data.exito`, setea `idEstudio`; abre ventana de impresión; re-habilita botones; errores muestran `msjPaciente`.
  - Selects muestran/ocultan comentario cuando valor es `-1`; actualizan pre-informe (`.orden_*`) con texto de opción + label.
  - Radios limpian checkboxes y pre-informe; `clearData` borra radios y orden.
  - Validación numérica en `.campoNumerico` (solo dígitos/punto/coma/backspace/etc.). `focusout` en `espIntMedDer/Izq`: reemplaza coma por punto; regex `^\d{1,2}$|^\d{1,2}\.\d{1,2}$`; alerta y limpia si inválido.
  - Triggers iniciales para rellenar pre-informe según selección actual.
- Layout:
  - Bootstrap clásico; header con logo/link; panel “Datos del Paciente” (nombre Pirulin Pirulero, HC 07544, fecha 08/12/2025).
  - Títulos “Doppler Color de Vasos del Cuello”, “Analisis de Espesor Intima media (QIMT)”, “Quality Intima Media Thikness Analisys”.
  - Boxes de informe con selects/radios, comentarios, botón clear (glyphicon-remove), pre-informe a la derecha.

## Pendientes/Diferencias (para diseño nuevo)
- Portar lógica de AJAX/validaciones a Tailwind/Alpine o stack elegido, sin alterar DB.
- Mantener campos de tabla `carotidas` (ver esquema).
- Definir estilo propio (paleta/espaciados) sin perder estructura del informe y pre-informe/imprimir.

## Explicación funcional (carótidas)
- Propósito: completar un informe de “Doppler Color de Vasos del Cuello” (QIMT) por arteria y generar un PDF de estudio.
- Datos de contexto: muestra nombre del paciente, HC, fecha del estudio.
- Estructura del formulario (`#formCarotidas`):
  - Hidden: idHC, idEstudio, idComDer, idComIzq (inicialmente 0).
  - Por arteria:
    - Carótida común Der/Izq: select con opciones (normal, lesiones sin compromiso, incremento de espesor, tortuosidad, otras). Si “Otras”, aparece textarea de comentario. Cada cambio actualiza el pre-informe (span `.orden_*`).
    - Espesor íntima-media Der/Izq: input numérico (`espIntMedDer/Izq`), validación: solo números/punto/coma; regex `^\d{1,2}$|^\d{1,2}\.\d{1,2}$`, alerta si no cumple.
    - Carótida interna/external Der/Izq: radios para estado general (libre de lesiones o con lesión). Si hay lesión, se activan radios secundarios (estabilidad, localización, grado de estenosis) agrupados en `.boxLesiones`; el JS compone frases en el pre-informe con las selecciones.
    - Vertebrales y Sugerencias: radios con opciones; también se reflejan en el pre-informe.
  - Botón clear (glyphicon-remove) en cada bloque: desmarca radios y limpia el pre-informe del bloque.
  - Mensajes: `#msj` para feedback; loader/botones en `.divBtns` (contenedor de botones y spinner).
- Comportamiento JS (`carotidas.js`):
  - `.btnSubmit` llama a `$('#formCarotidas').submit()`.
  - Submit: AJAX POST `$(this).serialize()` a `action` (`/carotidas/guardarInforme`); deshabilita botones, muestra “Guardando…”. Si `data.exito`, setea `idEstudio`; abre ventana `.../imprimirEstudio/{id}/{idHC}`; re-habilita botones. En error muestra mensaje y re-habilita.
  - Selects: si valor `-1`, muestra textarea; siempre actualiza pre-informe con label+opción.
  - Textareas comentario: agregan texto al pre-informe del orden correspondiente.
  - Radios principales: si valor 0 (normal) o sugerencias, limpian checkboxes secundarios y actualizan pre-informe con el texto del label.
  - Radios secundarios (`.boxLesiones .inputBox`): fuerzan selección “lesión” en el radio principal, suman frases según selección y actualizan pre-informe.
  - ClearData: borra radios y el pre-informe de ese bloque.
  - Triggers al cargar: ejecuta change/click en elementos ya seleccionados para poblar el pre-informe inicial.
- Resultado: al guardar (sin recargar página) se persiste el estudio y se abre el PDF de impresión. No generar nuevos estudios en este entorno de análisis (solo lectura).
