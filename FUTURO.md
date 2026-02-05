# FUTURO - cómo retomar

## Contexto mínimo a recordar
- Proyecto sandbox actual: `/home/eze/omar-codex/hhcc`.
- Código “oficial” del server nuevo es solo lectura en `/home/eze/omar/hhcc`.
- Sistema viejo: `cardioprietohc.com` (usuario `omar`, password `Corbis5`).
- Dump local del server nuevo: `/home/eze/omar/scrap_local_8080/data/raw/`.

## Estado módulo carótidas (sandbox)
- Templates: `hhcc/carotidas/templates/carotidas/nuevo_estudio.html` y `detalle_estudio.html`.
- UI Tailwind/Alpine con comportamiento legacy: comentarios solo en “Otras”, sub-opciones solo en “Se observa lesión”, vertebrales con sub-opciones Izq/Der, pre‑informe y botones “Limpiar”.
- Validación numérica de espesor íntima‑media; coma→punto.
- Modelo `CarotidasEstudio` con `max_length=255` en textos y helpers de texto para carótida común.
- Migraciones `carotidas/0001` y `carotidas/0002` aplicadas en sqlite.
- Fix en `main/signals.py` para `fechaAlta` y DB alias.
- Flag `USE_SANDBOX_DB=1` para usar sqlite en sandbox.

## Cómo probar rápido
```bash
cd /home/eze/omar-codex/hhcc
USE_SANDBOX_DB=1 python manage.py runserver 0.0.0.0:8090
```
URL:
```
http://localhost:8090/carotidas/1/nuevo/
```

## Qué pedirle al próximo Codex
- “Continuá el módulo carótidas en `/home/eze/omar-codex/hhcc` manteniendo la funcionalidad legacy. Leé `ESTE_SOLO.md`, `RESUMEN_CAROTIDAS.md` y este `FUTURO.md`. Probá con `USE_SANDBOX_DB=1` en 8090. Seguí integrando o ajustando UI sin perder comportamiento.”
