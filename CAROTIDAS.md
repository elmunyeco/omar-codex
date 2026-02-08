# CAROTIDAS (específico)

## Legacy (sitio viejo)
- Formulario: “Doppler Color de Vasos del Cuello” (`/index.php/carotidas/nuevoEstudio/{idHC}`).
- HTML autenticado de referencia: `Scrap_cardioprietohc/data/raw/carotidas/carotidas_7544_authed.html`.
- Assets legacy: `Scrap_cardioprietohc/data/raw/carotidas/assets/` (bootstrap, font‑awesome, `carotidas.css`, `jquery.min.js`, `carotidas.js`).

### Funcionalidad legacy (carotidas.js)
- Submit AJAX a `/carotidas/guardarInforme`:
  - Deshabilita botones, guarda, setea `idEstudio`, abre `imprimirEstudio/{id}/{idHC}`, re‑habilita.
  - Errores muestran mensaje.
- Dinámica de campos:
  - Carótida común Der/Izq: select + “Otras” con comentario.
  - Carótida interna/externa Der/Izq: radio “normal” vs “lesión” con sub‑radios (estabilidad, localización, estenosis).
  - Espesor íntima‑media Der/Izq: numérico con validación.
  - Vertebrales y sugerencias: radios.
  - Botón “Limpiar” por bloque.
- Pre‑informe: spans `.orden_*` actualizan con selecciones/comentarios.
- Validación numérica: regex `^\d{1,2}$|^\d{1,2}\.\d{1,2}$`, reemplazo coma→punto, alert si inválido.

### Tabla legacy
- `carotidas`:
  - `id`, `idHC`, `comDerecha`, `intDerecha`, `extDerecha`, `comIzquierda`, `intIzquierda`, `extIzquierda`,
  - `artVertebrales`, `sugerencias`, `idComDer`, `idComIzq`, `espIntMedDer`, `espIntMedIzq` (decimal 4,2).

## Estado actual en sandbox (`/home/eze/omar-codex/hhcc`)
- App `carotidas` funcional con Tailwind/Alpine (sin jQuery/Bootstrap).
- Templates:
  - `hhcc/carotidas/templates/carotidas/nuevo_estudio.html`
  - `hhcc/carotidas/templates/carotidas/detalle_estudio.html`

### Comportamiento preservado (ontológicamente igual al legacy)
- Comentarios en carótida común solo visibles si se elige “Otras”.
- Sub‑opciones solo visibles si se elige “Se observa lesión”.
- Vertebrales: sub‑opciones Izq/Der solo si se elige “Disminución del flujo…”.
- Pre‑informe en vivo con Alpine.
- Botones “Limpiar” por bloque (interna/externa der/izq, vertebrales, sugerencias).
- Validación espesor íntima‑media (regex + coma→punto).

### Modelo, form y helpers
- `CarotidasEstudio`:
  - textos `max_length=255` para no truncar.
  - helpers `com_der_texto()` y `com_izq_texto()`.
- `CarotidasForm`:
  - normaliza coma→punto y convierte a `Decimal`, agrega error si inválido.

### Migraciones y notas
- `carotidas/migrations/0001_initial.py`
- `carotidas/migrations/0002_alter_carotidasestudio_*.py`
- `main.0003` se aplicó `--fake` en sqlite por colisión de índices (`ind_hist_fecha_idx` ya existía).

## Cómo probar rápido
```bash
cd /home/eze/omar-codex/hhcc
USE_SANDBOX_DB=1 python manage.py runserver 0.0.0.0:8090
```
URL:
```
http://localhost:8090/carotidas/1/nuevo/
```

## Nota de infraestructura
- En sqlite ya existe una historia clínica demo con `id=1` para test.
- `USE_SANDBOX_DB=1` en `hhcc/settings.py` usa sqlite en lugar de MySQL.



## Impresión / PDF
- Se agregó endpoint de impresión en `carotidas`:
  - URL: `/carotidas/imprimir_estudio/<estudio_id>/<historia_id>/`
  - Vista: `carotidas.views.imprimir_estudio`.
  - Template: `hhcc/carotidas/templates/carotidas/imprimir_estudio.html`.
- En `nuevo_estudio.html` el submit ahora es AJAX: guarda y abre una nueva ventana con la impresión.
- PDF legacy descargado para referencia:
  - `Scrap_cardioprietohc/data/raw/carotidas/imprimirEstudio_4512_7544.pdf`


## Impresión (PDF)
- La impresión ahora genera PDF con WeasyPrint (no HTML).
- Se ocultan secciones sin datos: solo se renderiza lo completado.
- Endpoint: `/carotidas/imprimir_estudio/<estudio_id>/<historia_id>/` devuelve `application/pdf`.

- WeasyPrint sin base_url para evitar DisallowedHost en impresión.


## Impresión PDF
- Impresión PDF con WeasyPrint (no HTML).
- Se ocultan secciones vacías.
- Logo y site en header; texto sin errores ortográficos.
- Submit AJAX abre ventana con el PDF.


- Usa base común `hhcc/main/templates/print_base.html` para impresión.
- Divisores suaves entre membrete/títulos y títulos/informe.


- `print_base.html` es parametrizable (logo/site/header) vía contexto.


- `print_base.html` carga `print.css` para estilos comunes.
