# CARÓTIDAS / VASOS DEL CUELLO

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
- Botones “Limpiar” por bloque.
- Validación espesor íntima‑media (regex + coma→punto).

### Modelo, form y helpers
- `CarotidasEstudio`:
  - textos `max_length=255` para no truncar.
  - helpers `com_der_texto()` y `com_izq_texto()`.
  - campo `fecha_estudio` (DateField) para fecha de creación del estudio.
- `CarotidasForm`:
  - normaliza coma→punto y convierte a `Decimal`, agrega error si inválido.
  - override en form: `esp_int_med_der` / `esp_int_med_izq` como `CharField` para evitar error 400 en AJAX; conversión se mantiene en `clean()`.

### Migraciones y notas
- `carotidas/migrations/0001_initial.py`
- `carotidas/migrations/0002_alter_carotidasestudio_*.py`
- `main.0003` se aplicó `--fake` en sqlite por colisión de índices (`ind_hist_fecha_idx` ya existía).

## Impresión PDF
- Endpoint: `/carotidas/imprimir_estudio/<estudio_id>/<historia_id>/`.
- Respuesta `Content-Type: application/pdf` y `Content-Disposition: inline`.
- Se ocultan secciones sin datos (no imprime títulos vacíos).
- Logo y CSS se resuelven con `static_file_url()` (sin paths absolutos).
- Logo en membrete: `logo_omar_prieto.svg` con fallback a `logo.png`.
- Tamaño de logo en PDF: `.logo { height: 48px; max-width: 270px; object-fit: contain; }`.
- Sitio en header: `www.cardioprietohc.com`.
- Texto corregido sin errores ortográficos (p.ej. “Quality Intima Media Thickness Analysis”).
- No se imprime “Consultorio Cardiológico Doctores Prieto”; usar “Consultorio Cardiológico Doctor Omar Prieto”.
- WeasyPrint sin base_url para evitar `DisallowedHost`.
- Submit AJAX: guarda y abre nueva ventana con el PDF; popup se abre antes del fetch.
- Mensaje de éxito se muestra en el mismo evento AJAX (sin recarga).

## Template base de impresión
- Base común: `hhcc/main/templates/print_base.html`.
- Parametrizable por contexto: `print_logo_path`, `print_site_text`, `print_header_text`.
- Divisores suaves entre membrete/títulos y títulos/informe.
- Usa `print.css` para estilos comunes.

## URLs actuales
- Formulario base: `/carotidas/<historia_id>/`
- Crear estudio nuevo: `/carotidas/<historia_id>/?action=crear`
- Recuperar estudio específico: `/carotidas/<historia_id>/?action=recuperar&estudio=<id>`
- Listado simple (HTML sin estilo): `/carotidas/<historia_id>/estudios/`

## Referencias legacy
- PDF legacy descargado: `Scrap_cardioprietohc/data/raw/carotidas/imprimirEstudio_4512_7544.pdf`.

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
