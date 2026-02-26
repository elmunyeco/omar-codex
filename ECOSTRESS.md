# ECOSTRESS (Ecostrés cardíaco)

## Fuente / ubicación scrapeada
- URL autenticada: `https://cardioprietohc.com/index.php/stress/nuevoEstudio/7544`
- HTML guardado: `Scrap_cardioprietohc/data/raw/ecostress/ecostress_7544_authed.html`
- Assets: `Scrap_cardioprietohc/data/raw/ecostress/assets/`

## Header / branding (legacy)
- Logo: `https://cardioprietohc.com/images/logo.jpg`
- Link en header: `http://www.cardioprieto.com` (sin “hc” en el dominio, así viene en el HTML).

## Formulario (legacy)
- Form: `#formStress`
- Action: `/index.php/stress/guardarInforme`
- Hidden:
  - `idHC` (historia clínica)
  - `idEstudio` (0 si es nuevo)

### Campos superiores
- `indicacionEstudio` (text, max 40)
- `tipoApremio` (select): `Físico`, `Farmacológico`
- `medicacionMomentoEstudio` (text, max 50)
- `medicoSolicitante` (text, max 30)

### Datos de prueba ergométrica
- Frecuencia cardíaca:
  - `frecuenciaCardiacaBasal`
  - `frecuenciaCardiacaMaxima`
- Presión arterial (mmHg):
  - `presionArterialBasalInicial` / `presionArterialBasalFinal`
  - `presionArterialMaximaInicial` / `presionArterialMaximaFinal`

### Textareas clínicas
- `informeErgometria` (max 250) — trae texto por defecto en el HTML
- `datosEcocardiograficosBasales` (max 300)
- `datosEcocardiograficosPostEsfuerzoInmediato` (max 300)
- `conclusion` (max 300)

## JS (legacy)
- Archivo: `assets/js/stress.js`
- Lógica:
  - Click en `#btnSubmit`.
  - POST AJAX a `action` con `$('#formStress').serialize()`.
  - Si `data.id` no existe → error en `#msj`.
  - Si OK → `window.open('/stress/imprimirEstudio/{id}/{idHC}')`.
  - Deshabilita botones, muestra loader, re‑habilita al final.

## CSS (legacy)
- Archivo principal: `assets/css/stress.css`.
- Estilos relevantes:
  - `.header` centrado con logo.
  - `.tituloPrincipal` subrayado, 24px.
  - `.form-control` tamaño 12px.
  - `.boxComentario` oculto por default.
  - Loader `#ldgGuardar` con animación `glyphicon-refresh-animate`.

## Recursos descargados
- CSS: `bootstrap.css`, `bootstrap.min.css`, `style.css`, `font-awesome.min.css`, `stress.css`.
- JS: `jquery.min.js`, `jquery-1.9.0.min.js`, `stress.js`.
- Imágenes: `logo.jpg`, `icono.png`.
- Nota: quedó un artefacto en assets `assets/index.php/hClinica/verHClinica/7544` por el downloader (link no‑asset).

## Impresión (legacy)
- El JS abre: `/index.php/stress/imprimirEstudio/{id}/{idHC}`.
- Similar al flujo de carótidas: guardar → abrir PDF/impresión en nueva ventana.

## Implementación Django (sandbox)
- App nueva: `hhcc/ecostress` (registrada en `hhcc/hhcc/settings.py`).
- URLs:
  - Formulario: `/ecostress/<historia_id>/nuevo/`
  - PDF: `/ecostress/imprimir_estudio/<estudio_id>/<historia_id>/`
- Modelo: `EcostressEstudio` mapeado a tabla legacy `stress`.
  - PK: `id_stress` → columna `idStress`.
  - FK: `historia` → columna `idHC` (HistoriaClinica).
  - Campos textuales alineados a legacy: indicación, tipo de apremio, medicación, médico solicitante, frecuencias, presiones, informe, datos eco basales/post, conclusión.
  - Campo nuevo: `fecha_estudio` (DateField). En sqlite se agrega por migración `0002`.
- Migraciones:
  - `hhcc/ecostress/migrations/0001_initial.py`
  - `hhcc/ecostress/migrations/0002_ecostressestudio_fecha_estudio.py`
- Form + template:
  - Formulario Tailwind/Alpine en `hhcc/ecostress/templates/ecostress/nuevo_estudio.html`.
  - Defaults del legacy para `informeErgometria`, `datosEcocardiograficosBasales`, `datosEcocardiograficosPostEsfuerzoInmediato`, `conclusion`.
  - La fecha se setea automáticamente al guardar (fecha actual). No es editable en formulario.
  - `tipo_apremio` inicia en `Físico` (sin opción `:: Seleccionar ::`).
  - Submit AJAX abre popup antes del fetch (patrón de carótidas).
  - Mensaje de éxito se muestra en el mismo evento AJAX (sin recarga).
- Impresión:
  - `hhcc/ecostress/templates/ecostress/imprimir_estudio.html` extiende `print_base.html`.
  - WeasyPrint en `ecostress/views.py` (PDF inline).
  - Oculta secciones vacías (solo imprime si hay contenido).
  - Incluye la fecha en el membrete y en “Datos del estudio”.
  - Header usa `www.cardioprieto.com`.

## RAG
- HTML y assets ya guardados en `Scrap_cardioprietohc/data/raw/ecostress/`.
- Falta reindexar (dependencias de scraper no instaladas en este entorno).

## Notas
- No se crearon estudios nuevos (solo se descargó el formulario base).
- Si se requiere crear hasta 2 estudios para ver variantes de salida, hay que POSTear a `guardarInforme` con campos completos.

- RAG reindexado con `.venv_rag` en `Scrap_cardioprietohc`.
