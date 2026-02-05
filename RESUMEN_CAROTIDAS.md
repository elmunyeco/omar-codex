# Resumen módulo Carótidas

## Origen (sitio viejo)
- Formulario legacy: “Doppler Color de Vasos del Cuello” (`/index.php/carotidas/nuevoEstudio/{idHC}`), assets en `Scrap_cardioprietohc/data/raw/carotidas/` (HTML + CSS/JS/img).
- JS `carotidas.js`:
  - Submit AJAX a `/carotidas/guardarInforme`: deshabilita botones, guarda, setea `idEstudio`, abre ventana `imprimirEstudio/{id}/{idHC}`, re-habilita; errores muestran mensaje.
  - Campos: selects por carótida común (Der/Izq) con opción “otras” + comentario; radios por carótida interna/externa (Der/Izq) con sub-radios (lesión, estabilidad, localización, estenosis); espesor íntima-media (Der/Izq) con validación numérica; vertebrales y sugerencias; botones clear por bloque.
  - Pre-informe: actualiza spans `.orden_*` según selecciones/comentarios; triggers iniciales poblando con valores seleccionados.
  - Validación numérica: solo dígitos/punto/coma; regex `^\d{1,2}$|^\d{1,2}\.\d{1,2}$`; alerta si inválido.
  - Layout: Bootstrap clásico, panel datos paciente, títulos QIMT, boxes con selects/radios, pre-informe a la derecha.
- Tabla legacy: `carotidas` (id, idHC, comDerecha/Izquierda, int/ext Der/Izq, artVertebrales, sugerencias, idComDer/Izq, espIntMedDer/Izq).

## Estado actual en este sandbox (`/home/eze/omar-codex/hhcc`)
- App `carotidas` funcional con Tailwind/Alpine (sin jQuery/Bootstrap).
- Templates creados:
  - `hhcc/carotidas/templates/carotidas/nuevo_estudio.html`
  - `hhcc/carotidas/templates/carotidas/detalle_estudio.html`
- Comportamiento preservado (ontológicamente igual al legacy, simplificado visualmente):
  - Comentarios en carótida común solo visibles cuando se elige “Otras”.
  - Sub-opciones (estabilidad/localización/estenosis) solo visibles cuando se elige “Se observa lesión”.
  - Arterias vertebrales: se elige “Disminución del flujo…” y recién ahí aparece izquierda/derecha; se construye texto final.
  - Pre‑informe en vivo con Alpine, basado en las selecciones y textos.
  - Botones “Limpiar” por bloque (interna/externa der/izq, vertebrales, sugerencias) con reset completo del estado.
  - Validación de espesor íntima-media (regex, reemplazo coma→punto, alerta si inválido).
- Modelo `CarotidasEstudio`:
  - Campos de texto ampliados a `max_length=255` para no truncar frases.
  - Helpers `com_der_texto()` y `com_izq_texto()` para mapear `id_com_*` a texto.
- Form `CarotidasForm`:
  - Normaliza coma→punto y convierte a `Decimal`, agrega error si inválido.
- Migraciones:
  - `carotidas/migrations/0001_initial.py`
  - `carotidas/migrations/0002_alter_carotidasestudio_*.py`
- Fix en señales:
  - `main/signals.py`: usa `fechaAlta`, respeta alias de DB y borra correctamente al fallar.
- Config de DB para sandbox:
  - En `hhcc/hhcc/settings.py` se agregó `USE_SANDBOX_DB=1` para usar sqlite (`db.sqlite3`).
  - En sqlite se aplicaron migraciones y se creó una historia clínica demo con `id=1`.

## Cómo probar (sandbox)
```bash
cd /home/eze/omar-codex/hhcc
USE_SANDBOX_DB=1 python manage.py runserver 0.0.0.0:8090
```
URL:
```
http://localhost:8090/carotidas/1/nuevo/
```

## Notas de migración
- La migración `main.0003` se aplicó como `--fake` en sqlite por colisión de índices (`ind_hist_fecha_idx` ya existía).

## RAG/Assets
- Lo scrapeado está indexable; headless en este entorno falla por sandbox (usar curl/requests o headless en otro host).
