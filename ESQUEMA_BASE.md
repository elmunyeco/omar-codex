# ESQUEMA BASE (MySQL, solo lectura)

## Conexion
- Host: `127.0.0.1`
- Puerto: `3307`
- DB: `cardioprieto`
- Usuario: `root`
- Password: `Corbis5`
- Acceso usado: **solo lectura** (`SHOW` / `DESCRIBE`).

## Tablas (resumen)
- Pacientes / historias:
  - `pacientes`, `historias_clinicas`, `tipos_documentos`
  - `condiciones_medicas`, `condiciones_medicas_historias`
  - `signos_vitales`
  - `comentarios_visitas`
  - `indicaciones_visitas`
- Estudios legacy (a reemplazar por omar-codex):
  - `carotidas`
  - `doppler` (MMII)
  - `stress` (ecostress)
- Otros: `pacientes_backup`, `random_hc`, tablas auth/django.

## Esquema (campos clave)
### pacientes
- `id` (PK)
- `idTipoDoc_id`, `numDoc`, `nombre`, `apellido`, `fechaNac`, `sexo`
- `mail`, `direccion`, `localidad`, `obraSocial`, `plan`, `afiliado`
- `telefono`, `celular`, `profesion`, `referente`
- `fechaAlta`, `deBaja`

### historias_clinicas
- `id` (PK)
- `fechaAlta`
- `paciente_id` (FK)

### signos_vitales
- `id` (PK)
- `historia_id` (FK)
- `fecha`
- `presion_sistolica`, `presion_diastolica`, `peso`, `glucemia`, `colesterol`

### comentarios_visitas
- `id` (PK)
- `idHistoriaClinica` (FK)
- `fecha` (datetime)
- `comentarios` (longtext)
- `tipo` (EVOL/INDIC)

### indicaciones_visitas
- `id` (PK)
- `historia_clinica_id` (FK)
- `medicamento`, `ochoHoras`, `doceHoras`, `dieciochoHoras`, `veintiunaHoras`
- `fecha`, `eliminado`

### condiciones_medicas / condiciones_medicas_historias
- `condiciones_medicas`: `id`, `nombre`, `orden`
- `condiciones_medicas_historias`: `historia_id`, `condicion_id`

## Estudios legacy (a reemplazar)
### carotidas
- Campos principales: `com_derecha`, `int_derecha`, `ext_derecha`, `com_izquierda`, `int_izquierda`, `ext_izquierda`
- `art_vertebrales`, `sugerencias`, `esp_int_med_der`, `esp_int_med_izq`
- `historia_id` (FK)

### doppler (MMII)
- `idDoppler` (PK)
- Textos arteriales (longtext) + `conclusion`
- `idHC` (FK)

### stress (ecostress)
- `idStress` (PK)
- Indicacion, tipo apremio, medicacion, medico solicitante, frecuencias, presiones
- `informeErgometria`, `datosEcocardiograficosBasales`, `datosEcocardiograficosPostEsfuerzoInmediato`, `conclusion`
- `idHC` (FK), `fecha_estudio`

## Regla de reemplazo
- Carotidas, Doppler/MMII y Stress/Ecostress en MySQL se **reemplazan** por los estudios de `/home/eze/omar-codex`.
- Ecocardiograma se **incorpora** desde `/home/eze/omar-codex`.

