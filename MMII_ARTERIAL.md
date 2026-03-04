# DOPPLER COLOR ARTERIAL DE MIEMBROS INFERIORES (MMII)

## Fuente / ubicación scrapeada
- URL autenticada: `https://cardioprietohc.com/index.php/doppler/nuevoEstudio/7544`
- HTML guardado: `Scrap_cardioprietohc/data/raw/mmii/doppler_7544_authed.html`
- Assets: `Scrap_cardioprietohc/data/raw/mmii/assets/`

## Header / branding (legacy)
- Logo: `https://cardioprietohc.com/images/logo.jpg`
- Link en header: `http://www.cardioprieto.com`

## Formulario (legacy)
- Form: `#formDoppler`
- Action: `/index.php/doppler/guardarInforme`
- Hidden:
  - `idHC` (historia clínica)
  - `idEstudio` (0 si es nuevo)

### Campos (textareas)
Sistema arterial derecho (max 300):
- `artFemComunDerechas`
- `artFemSuperficialDerechas`
- `artFemProfundaDerechas`
- `artPopliteaDerechas`
- `artInfrapatelaresDerechas`

Sistema arterial izquierdo (max 300):
- `artFemComunIzquierdas`
- `artFemSuperficialIzquierdas`
- `artFemProfundaIzquierdas`
- `artPopliteaIzquierdas`
- `artInfrapatelaresIzquierdas`

Conclusiones (max 500):
- `conclusiones`

### Defaults legacy
- Texto estándar de arterias:
  - “Arteria con estructura conservada libre de deformaciones. Análisis espectral acorde al vaso de estudio. Velocidades máximas dentro de los límites normales.”
- Conclusión por defecto:
  - “Estudio arterial de miembros inferiores dentro de límites normales.”

## JS (legacy)
- Archivo: `assets/js/doppler.js`
- Lógica:
  - Click en `#btnSubmit`.
  - POST AJAX a `action` con `$('#formDoppler').serialize()`.
  - Si OK → abre `imprimirEstudio/{id}/{idHC}` en nueva ventana.
  - Deshabilita botones y muestra loader mientras guarda.

## CSS (legacy)
- Usa `bootstrap.css`, `font-awesome.min.css` y `carotidas.css`.

## Tabla legacy (renombrada)
- `mmii` (antes `doppler`):
  - `idMMII` (PK) (antes `idDoppler`)
  - `idHC` (FK historia)
  - `artFemComunDerecha`
  - `artFemSuperficialDerecha`
  - `artFemProfundaDerecha`
  - `artPopliteaDerecha`
  - `artInfrapatelaresDerecha`
  - `artFemComunIzquierda`
  - `artFemSuperficialIzquierda`
  - `artFemProfundaIzquierda`
  - `artPopliteaIzquierda`
  - `artInfrapatelaresIzquierda`
  - `conclusion`

## Implementación Django (sandbox)
- App nueva: `hhcc/mmii` (registrada en `hhcc/hhcc/settings.py`).
- URLs:
  - Formulario base: `/mmii/<historia_id>/`
  - Crear estudio nuevo: `/mmii/<historia_id>/?action=crear`
  - Recuperar estudio específico: `/mmii/<historia_id>/?action=recuperar&estudio=<id>`
  - Listado simple (HTML sin estilo): `/mmii/<historia_id>/estudios/`
  - PDF: `/mmii/imprimir_estudio/<estudio_id>/<historia_id>/`
- Modelo: `MmiiEstudio` mapeado a tabla `mmii`.
  - PK: `id_mmii` → columna `idMMII`.
  - FK: `historia` → columna `idHC` (HistoriaClinica).
  - Campos textuales alineados a legacy para todas las arterias y conclusión.
  - Campo nuevo: `fecha_estudio` (DateField) para fecha de creación del estudio.
- Migraciones:
  - `hhcc/mmii/migrations/0001_initial.py`
  - `hhcc/mmii/migrations/0002_migrate_from_doppler.py` (migra data y elimina tabla `doppler`)
- Form + template:
  - Formulario Tailwind/Alpine en `hhcc/mmii/templates/mmii/nuevo_estudio.html`.
  - Defaults del legacy para todas las arterias y conclusión.
  - Submit AJAX abre popup antes del fetch (patrón de carótidas/ecostress).
  - Mensaje de éxito se muestra en el mismo evento AJAX (sin recarga).
- Impresión:
  - `hhcc/mmii/templates/mmii/imprimir_estudio.html` extiende `print_base.html`.
  - WeasyPrint en `mmii/views.py` (PDF inline).
  - Secciones separadas para sistema derecho/izquierdo y conclusiones.
  - Fecha del estudio: `fecha_estudio` con formato `j de F de Y`.
  - Logo y CSS se resuelven con `static_file_url()` (sin paths absolutos).
  - Logo en membrete: `logo_omar_prieto.svg` con fallback a `logo.png`.
  - Tamaño de logo en PDF: `.logo { height: 48px; max-width: 270px; object-fit: contain; }`.

## RAG
- HTML y assets guardados en `Scrap_cardioprietohc/data/raw/mmii/`.
- Índice reindexado: `Scrap_cardioprietohc/data/cache/rag_index.pkl`.

## Cómo probar rápido
```bash
cd /home/eze/omar-codex/hhcc
USE_SANDBOX_DB=1 python manage.py runserver 0.0.0.0:8090
```
URL:
```
http://localhost:8090/mmii/1/nuevo/
```
