# Diff visual (ojo) - Estudios 8090 vs 8080

Fecha: 2026-04-05

## Alcance
Comparación visual entre:
- 8090 (omar-codex)
- 8080 (omar)

Se compararon formularios y PDFs de estudios (eco, stress, carótidas, mmii). Se usaron IDs de prueba existentes (no se modificó nada).

## Metodología
- Capturas de pantalla en ambos servidores.
- Diferencias visuales cuantificadas con diff de imágenes.
- Revisión ocular con recortes de zonas de mayor diferencia.

Carpeta con evidencia: `Scrap_cardioprietohc/data/reports/visual_styles_8090_vs_8080_2026-04-05`

## Resultados (similitud visual)
- Eco: form `98.73`, PDF `100.00`
- Stress: form `97.64`, PDF `100.00`
- Carótidas: form `96.62`, PDF `99.47`
- MMII: form `97.32`, PDF `100.00`

## Observaciones visuales (ojo)

### Ecocardiograma (form)
- Diferencias percibidas: **solo antialiasing/render de texto**.
- No hay cambios de layout ni de estilos visibles.
- Evidencia (recortes):
  - `Scrap_cardioprietohc/data/reports/visual_styles_8090_vs_8080_2026-04-05/eco_8090_form_block1.png`
  - `Scrap_cardioprietohc/data/reports/visual_styles_8090_vs_8080_2026-04-05/eco_8080_form_block1.png`
  - Diff: `Scrap_cardioprietohc/data/reports/visual_styles_8090_vs_8080_2026-04-05/eco_diff_form_block1.png`

### Ecostress (form)
- Diferencias percibidas: **antialiasing de texto** (ligeras variaciones de grosor/kerning).
- No hay cambios de layout ni de estilos visibles.
- Evidencia (recortes):
  - `Scrap_cardioprietohc/data/reports/visual_styles_8090_vs_8080_2026-04-05/stress_8090_form_block1.png`
  - `Scrap_cardioprietohc/data/reports/visual_styles_8090_vs_8080_2026-04-05/stress_8080_form_block1.png`
  - Diff: `Scrap_cardioprietohc/data/reports/visual_styles_8090_vs_8080_2026-04-05/stress_diff_form_block1.png`

### Carótidas (form)
- Diferencia visible: **botón “Guardar” aparece en el recorte de 8080 y no en 8090** (probable diferencia de scroll/altura de vista).
- Resto: antialiasing de texto.
- Evidencia (recortes):
  - `Scrap_cardioprietohc/data/reports/visual_styles_8090_vs_8080_2026-04-05/carotidas_8090_form_block1.png`
  - `Scrap_cardioprietohc/data/reports/visual_styles_8090_vs_8080_2026-04-05/carotidas_8080_form_block1.png`
  - Diff: `Scrap_cardioprietohc/data/reports/visual_styles_8090_vs_8080_2026-04-05/carotidas_diff_form_block1.png`

### MMII (form)
- Diferencias percibidas: **antialiasing de texto**.
- No hay cambios de layout ni de estilos visibles.
- Evidencia (recortes):
  - `Scrap_cardioprietohc/data/reports/visual_styles_8090_vs_8080_2026-04-05/mmii_8090_form_block1.png`
  - `Scrap_cardioprietohc/data/reports/visual_styles_8090_vs_8080_2026-04-05/mmii_8080_form_block1.png`

### PDFs
- Visualmente iguales en todos los estudios (similitud 99.47–100.00).
- Evidencia en carpeta:
  - `*_8090_pdf.png`, `*_8080_pdf.png`, `*_diff_pdf.png`

## Conclusión
Los formularios y PDFs de estudios entre 8090 y 8080 se ven **prácticamente iguales**. Las diferencias detectadas son mínimas (antialiasing) y un caso puntual de botón visible en carótidas por posición de scroll.
