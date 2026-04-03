# TODO - Historial Médico / Signos Vitales (UI)

## Problema
El formulario de signos vitales representa **una nueva visita** y por eso aparece vacío. Eso es correcto a nivel de modelo, pero es mala UX: obliga a reingresar valores habituales en cada visita.

## Propuesta (sin cambiar el modelo actual)
- Mantener el comportamiento de “crear nueva visita”.
- **Pre‑llenar con los últimos valores conocidos** y señalizar que fueron copiados de la última visita.

## Opciones de implementación
- Botón `Usar última visita` que auto‑rellena los campos.
- Toggle `Autorellenar al abrir` (ON por defecto).
- Panel lateral `Últimos valores` con click para copiar cada campo.

## Resultado esperado
Mejora de usabilidad sin modificar la persistencia (cada guardado sigue creando un nuevo registro).
