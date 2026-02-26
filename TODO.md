# TODO

## Impresión (Ecocardiograma)
- [ ] Generar PDF real (WeasyPrint) como carótidas.
- [ ] Ocultar secciones vacías en impresión PDF (solo renderizar lo completado).

## ECOSTRESS
- [x] Implementar app Django `ecostress` (modelo, form, vistas, templates, PDF).
- [ ] Si se requiere, crear hasta 2 estudios en legacy para capturar variantes de impresión.

## MMII
- [x] Renombrar app `doppler` a `mmii` (urls, templates, assets, DB).

## RAG / Data
- [x] Agregar PDF legacy de carótidas a `Scrap_cardioprietohc/data/raw/`.
- [ ] Agregar cualquier otro PDF/HTML faltante al RAG.
- [x] Reindexar RAG si se agregan nuevos PDFs/HTML (`python -m scrap_cardioprietohc.cli rag-index --source data/raw --index data/cache/rag_index.pkl`).

## Pacientes (Scraper vs Django)

### Issues actuales
- Stack/UI: Tailwind + Alpine es preferible al Bootstrap/jQuery del sitio original, pero hay que alinear flujos y datos para no perder funcionalidad.
- Datos y campos:
  - Lista usa `paciente.dni` (no existe); debería mostrar `paciente.numDoc`.
  - Formularios usan sexo `M/F`; modelo/DB usan `H/M` (riesgo de inconsistencias).
- Flujos vs original:
  - Lista actual: búsqueda GET, solo acción editar; falta eliminar y feedback/mensajes tipo `funciones.js`. Original: POST `/pacientes/buscador`, reemplaza tbody y oculta paginador, botón “Eliminar filtros”, acción eliminar (AJAX) que borra fila.
  - Paginación actual Django estándar; original `/pacientes/listar/{page}` y se oculta al buscar.
  - Formularios actuales: submit tradicional sin AJAX/mensajes/loader; original usa `funciones.js` con alta/edición AJAX, mensajes éxito/error, post-alta (link a HC).
- Estilo/UX:
  - Paleta actual (#9a4035) vs original (acento rojo `#D9100C`, fondo rojo semitransparente en menú activo, borde izq).
  - Layout original: form-horizontal (label col-4 + input col-4) apilado; buscador con paddings (left 40, botón alta derecha), tabla con editar/eliminar y glyphicons.
  - Nuevo UI puede mantenerse, pero recuperar: acción eliminar, mensajes de estado, cálculo de edad, feedback de búsqueda.

### Objetivos de UI/UX (módulos nuevos)
- Mayor limpieza visual: paleta acotada, menos dispersión de colores.
- Menos distracción/ruido: eliminar menús/caminos redundantes; foco en la tarea principal.
- Consolidar patrones de navegación y feedback (mensajes, loaders, estados) en todas las pantallas.
- Una vez estabilizados módulos nuevos, completar funcionalidad y homogeneizar UI + flujos con las decisiones tomadas.

### Tareas
- [x] Copiar el scraper bueno (`/home/eze/culo/Scrap_cardioprietohc`) a `/home/eze/omar-codex` sin `.venv`.
- [ ] Recrear venv, Playwright e índice RAG en `/home/eze/omar-codex/Scrap_cardioprietohc`.
- [ ] Corregir campos en Django: `numDoc` en la lista; sexo `H/M` en formularios (ver impacto en datos).
- [ ] Decidir flujo de búsqueda/eliminar: mantener GET o clonar flujo original (POST buscador, AJAX reemplazo tbody, paginador removido, eliminar fila).
- [ ] Añadir acción eliminar en la lista (fetch/Alpine) y feedback de búsqueda/errores similar a `funciones.js`.
- [ ] Portar validaciones/UX útiles de `funciones.js` a Alpine/fetch (mensajes, cálculo edad, estados post-alta/edición).
- [ ] Alinear estilos (sidebar activo, buscador, botón alta, tabla, iconografía) manteniendo el diseño Tailwind pero con la jerarquía del original.

### Arreglar bugs
- [ ] En todos los estudios cambiar la fecha por la fecha de generacion de estudio, y la que ahora figura, que hay que averiguar de donde sale, ponerla como "fecha de impresion" en el footer.
