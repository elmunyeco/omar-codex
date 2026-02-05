# Resumen módulo Carótidas

- Origen (sitio viejo): formulario “Doppler Color de Vasos del Cuello” (`/index.php/carotidas/nuevoEstudio/{idHC}`), con assets descargados en `Scrap_cardioprietohc/data/raw/carotidas/` (HTML autenticado + CSS/JS/img). JS `carotidas.js` maneja:
  - Submit AJAX a `/carotidas/guardarInforme`: deshabilita botones, guarda, setea `idEstudio`, abre ventana `imprimirEstudio/{id}/{idHC}`, re-habilita; errores muestran mensaje.
  - Campos: selects por carótida común (Der/Izq) con opción “otras” + comentario; radios por carótida interna/externa (Der/Izq) con sub-radios (lesión, estabilidad, localización, estenosis); espesor íntima-media (Der/Izq) con validación numérica; vertebrales y sugerencias; botones clear por bloque.
  - Pre-informe: actualiza spans `.orden_*` según selecciones/comentarios; triggers iniciales poblando con valores seleccionados.
  - Validación numérica: solo dígitos/punto/coma; regex `^\d{1,2}$|^\d{1,2}\.\d{1,2}$`; alerta si inválido.
  - Layout: Bootstrap clásico, panel datos paciente, títulos QIMT, boxes con selects/radios, pre-informe a la derecha.
- Tabla legacy: `carotidas` (id, idHC, comDerecha/Izquierda, int/ext Der/Izq, artVertebrales, sugerencias, idComDer/Izq, espIntMedDer/Izq).

- Django nuevo: app `hhcc/carotidas` creada (modelo `CarotidasEstudio` alineado a la tabla; forms/views/urls/admin; templates pendientes). Rutas: `/carotidas/<historia_id>/nuevo/`, `/carotidas/estudio/<pk>/`.

- RAG/Assets: lo scrapeado está indexable; headless en este entorno falla por sandbox (usar curl/requests o headless en otro host).
