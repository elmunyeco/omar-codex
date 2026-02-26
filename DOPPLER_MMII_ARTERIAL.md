# DOPPLER COLOR ARTERIAL DE MIEMBROS INFERIORES

## Fuente / ubicación scrapeada
- URL autenticada: `https://cardioprietohc.com/index.php/doppler/nuevoEstudio/7544`
- HTML guardado: `Scrap_cardioprietohc/data/raw/doppler/doppler_7544_authed.html`
- Assets: `Scrap_cardioprietohc/data/raw/doppler/assets/`

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

## Tabla legacy
- `doppler`:
  - `idDoppler` (PK)
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
- App nueva: `hhcc/doppler` (registrada en `hhcc/hhcc/settings.py`).
- URLs:
  - Formulario: `/doppler/<historia_id>/nuevo/`
  - PDF: `/doppler/imprimir_estudio/<estudio_id>/<historia_id>/`
- Modelo: `DopplerEstudio` mapeado a tabla legacy `doppler`.
  - PK: `id_doppler` → columna `idDoppler`.
  - FK: `historia` → columna `idHC` (HistoriaClinica).
  - Campos textuales alineados a legacy para todas las arterias y conclusión.
- Migraciones:
  - `hhcc/doppler/migrations/0001_initial.py`
- Form + template:
  - Formulario Tailwind/Alpine en `hhcc/doppler/templates/doppler/nuevo_estudio.html`.
  - Defaults del legacy para todas las arterias y conclusión.
  - Submit AJAX abre popup antes del fetch (patrón de carótidas/ecostress).
- Impresión:
  - `hhcc/doppler/templates/doppler/imprimir_estudio.html` extiende `print_base.html`.
  - WeasyPrint en `doppler/views.py` (PDF inline).
  - Secciones separadas para sistema derecho/izquierdo y conclusiones.
  - Fecha del estudio: `timezone.localdate()`.

## RAG
- HTML y assets guardados en `Scrap_cardioprietohc/data/raw/doppler/`.
- Índice reindexado: `Scrap_cardioprietohc/data/cache/rag_index.pkl`.

## Cómo probar rápido
```bash
cd /home/eze/omar-codex/hhcc
USE_SANDBOX_DB=1 python manage.py runserver 0.0.0.0:8090
```
URL:
```
http://localhost:8090/doppler/1/nuevo/
```
