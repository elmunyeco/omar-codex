# Checklist de Cierre – Sistema Local (2026-03-26)

## A) Consolidación de pantallas core
- [ ] Confirmar plantilla canónica de HC: `detalle_historia_con_historial_2.html`.
- [ ] Eliminar/archivar `detalle_historia_con_historial.html` y asegurar que ninguna URL la use.
- [ ] Verificar que `listar_buscar_historias_2.html` apunte a la plantilla canónica.

## B) Órdenes vs Solicitudes (unificación)
- [ ] Elegir **un solo flujo**: usar `ordenes_pedicas` como canónico.
- [ ] Menú: reemplazar “Órdenes Médicas” por “Solicitudes” (legacy) y apuntar a `ordenes_pedicas`.
- [ ] Redirigir `ordenes_medicas` → `ordenes_pedicas` **o** eliminar la ruta y template duplicado.
- [ ] Validar generación de PDFs con `generar_pdf_orden`.

## C) Limpieza de duplicados
- [ ] Revisar `hhcc/main/new_templates/` y `hhcc/main/old_templates/` y archivar lo no usado.
- [ ] Asegurar que templates activos estén solo en `hhcc/main/templates/`.

## D) Comentarios / Visitas
- [ ] Confirmar regla: una visita por día (si hay dos, editar la primera).
- [ ] Validar comentarios con precisión a nivel **día**.
- [ ] Verificar eliminación de comentarios en local (endpoint JSON) desde UI.

## E) QA funcional core
- [ ] Pacientes: listar, crear, editar, eliminar.
- [ ] Historias clínicas: listar, paginar, abrir detalle.
- [ ] HC detalle: comentarios, signos vitales, condiciones (acciones embebidas).
- [ ] Indicaciones: listado, agregar, comentario, eliminar.
- [ ] Solicitudes: generar PDF de estudios.

### Notas QA (2026-04-03)
- TEST_QA_1 creado y editado (obraSocial=QA_OBRA, telefono=123456). Se deja en base.
- TEST_QA_2 creado. Eliminación **bloqueada** porque al crear paciente se genera HistoriaClinica (signal) y la UI no permite borrar con HC asociada.
- Intento de borrar HC de TEST_QA_2 falla por dependencia a tabla `estudios_ecocardiograma` inexistente en DB local.
- Se decide **no cambiar** el comportamiento (mantener HC para auditoría/legal).

## F) Idempotencia UI
- [ ] Reejecutar test UI solo con ID 7544.
- [ ] Confirmar idempotencia por pantalla core.

### Resultado F (2026-04-03)
- Ejecutado `idempotency_ui_7544.py` (CDP 9992 + local 8080).
- Legacy: comentarios_count sube [54, 55, 56] (no idempotente para comentarios).
- Legacy: signos peso sin cambios [3, 3, 3].
- Local: visitas_count [13, 14, 14] (idempotente en segunda pasada).
- Local: comentario queda igual en segunda pasada (idempotente).

## G) Documentación
- [ ] Actualizar `plan_cierre_local_2026-03-26.md` si hay cambios de alcance.
- [ ] Mantener `legacy_vs_local_use_cases_2026-03-26.*` como documento auditado.

## H) Integración estudios (pendiente)
- [ ] No tocar módulos de estudios hasta integrar local + local-estudios.
- [ ] Definir plan de integración cuando ambos repos estén listos.
