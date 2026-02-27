# ECOCARDIOGRAMA (impresión)

## Base de impresión
- El template de impresión extiende `print_base.html` para homogeneidad.
- Usa logo, site y header parametrizados via contexto.
- `print_base.html` carga `print.css` para estilos comunes.

## Estilo sin Tailwind
- Se removieron clases Tailwind en impresión.
- El layout usa CSS propio (tablas, grilla, firma, botones de impresión).
- Títulos y secciones usan los mismos separadores y jerarquía que carótidas.

## Archivos clave
- `hhcc/ecocardiograma/templates/ecocardiograma/imprimir_estudio.html`
- `hhcc/ecocardiograma/views.py` (pasa `print_logo_path`, `print_site_text`, `print_header_text`).

## Migraciones
- `hhcc/ecocardiograma/migrations/0001_initial.py`

## Motilidad segmentaria (miniapp)
- Archivo: `hhcc/ecocardiograma/segmentos.html`
- Copia estática: `hhcc/ecocardiograma/static/ecocardiograma/segmentos.html`
- Estado inicial: todos los segmentos inician en **Normal** (estado `1`).
- Botón "Marcar Todos Normales":
  - Inicia deshabilitado si todo está en Normal.
  - Se habilita al cambiar cualquier segmento.
  - Se vuelve a deshabilitar al marcar todo como Normal.

## Legacy (eco/verEstudio) - scrape y RAG
- HTML legacy: `Scrap_cardioprietohc/data/raw/ecocardiograma/eco_verEstudio_5759_7544.html`
- Assets legacy: `Scrap_cardioprietohc/data/raw/ecocardiograma/assets/`
- RAG: `Scrap_cardioprietohc/data/cache/rag_index.pkl` (reindexado con el material de ecocardiograma)

## Módulo (integración actual)
- Tab “Motilidad Segmentaria” en `hhcc/ecocardiograma/templates/ecocardiograma/eco_form.html` ahora usa iframe con la miniapp.
- Sincronización:
  - La miniapp expone `__ecoSegmentosGet/__ecoSegmentosSet` y emite `__ecoSegmentosSync`.
  - El form principal escucha `__ecoSegmentosSync` y actualiza `segmentos` + autosave.
  - Antes de guardar, se sincroniza desde el iframe para no perder cambios.
- Default legacy: segmentos inicializan en **Normal** (`1`).
- Conclusiones legacy completas (Situs, Vasos, Concordancia, Valvulares con selección múltiple y comentarios).
- Fix: `historiaId` puede llegar `null` en `guardar_todo_ajax`; se agregó `data-historia-id` y fallback en `inicializar()` + guard en `guardarDatos()`.

## Endpoints legacy implementados
- `ecocardiograma/guardarPaciente`
- `ecocardiograma/guardarBidimensional`
- `ecocardiograma/guardarCoppler`
- `ecocardiograma/guardarSegmentos`
- `ecocardiograma/guardarConclusiones`
- `ecocardiograma/guardarConclusionB`
- `ecocardiograma/guardarComentarioFinal`

## Mapeo legacy (items 1..14)
- 1: aurícula izquierda (`auricula_izq`)
- 2: ventrículo izquierdo (`ventriculo_izq`)
- 3: función sistólica (`funcion_sistolica`)
- 4: función diastólica (`funcion_diastolica`)
- 5: motilidad segmentaria (`motilidad_segmentaria`) + `comentario_motilidad`
- 6: válvula aórtica (`valvula_aortica`) + `comentario_valvula_aortica`
- 7: válvula mitral (`valvula_mitral`) + `comentario_valvula_mitral`
- 8: válvula tricúspide (`valvula_tricuspide`) + `comentario_valvula_tricuspide`
- 9: válvula pulmonar (`valvula_pulmonar`) + `comentario_valvula_pulmonar`
- 10: pericardio (`pericardio`) + `comentario_pericardio`
- 11: defectos congénitos (`defectos_congenitos`) + `comentario_defectos`
- 12: situs (`situs`) + `comentario_situs`
- 13: vasos normo implantados (`vasos_normoimplantados`) + `comentario_vasos`
- 14: concordancia atrioventricular (`concordancia_atrioventricular`) + `comentario_concordancia`

## Impresión
- Secciones vacías se omiten.
- Motilidad segmentaria imprime detalle de segmentos (1..16) y si todos están en normal agrega “Normoquinetico”.
- Conclusión B y Comentario Final se imprimen solo si tienen contenido.
- Impresión usa assets estáticos (logo y CSS) vía `{% static %}` para que el navegador renderice el estilo correctamente.
- Imagen de segmentos para impresión: `hhcc/ecocardiograma/static/ecocardiograma/images/segmentos.png`.
- Impresión ahora se genera con WeasyPrint (como carótidas/ecostress/mmii), sin página intermedia de “Imprimir”.
- Motilidad segmentaria: tabla sin títulos ni bordes, 4 columnas, fuente reducida para no desbordar.
- El gráfico impreso incluye la capa de color de segmentos según estado (mismos colores que el formulario).
- Fix: en `imprimir_estudio` se corrigió el armado de `segmentos_detalle/segmentos_colores` para que el SVG no quede en blanco.
- Ajuste: tabla de segmentos compacta debajo del gráfico, con nombre y estado en dos líneas por celda.
- Se quitó la firma final (línea + “Dr. Omar Prieto / Cardiólogo”) del PDF.
- Pie de página común (en `print_base.html`): 2 renglones en blanco, línea divisoria, “Emitido DD/MM/AAAA” a la izquierda, “Dr. Omar Prieto” a la derecha, y “cardiologo” alineado a la derecha debajo.

## UI (formulario)
- Botón principal: texto “Guardar” (antes “Guardar e Imprimir”).
- Botón de imprimir del header y botón “Volver” quedaron comentados para ocultarlos.
