# Checklist QA Post-Integracion

Fecha: 2026-04-04

## 1) Acceso y navegacion
- [ ] Login funciona (usuario valido / invalidos).
- [ ] Logout funciona y redirige.
- [ ] Menu principal carga sin errores JS.

## 2) Pacientes
- [ ] Listado de pacientes abre.
- [ ] Busqueda por DNI / apellido funciona.
- [ ] Crear paciente y validar datos basicos.
- [ ] Editar paciente.
- [ ] Eliminar paciente (si aplica).

## 3) Historias Clinicas
- [ ] Listado de historias abre.
- [ ] Crear historia clinica.
- [ ] Editar historia clinica.
- [ ] Historial medico (visitas) carga.
- [ ] Comentarios / indicaciones se guardan.
- [ ] Regla de una visita por dia: edita la primera si hay duplicadas.

## 4) Solicitudes / Ordenes Medicas
- [ ] Ruta Solicitudes abre desde menu.
- [ ] Crear solicitud con diagnostico + estudios.
- [ ] PDF de solicitud se genera (WeasyPrint).

## 5) Estudios (UI)
- [ ] Ecocardiograma abre (HC con estudio existente).
- [ ] Ecostress abre (HC con estudio existente).
- [ ] Carotidas abre (HC con estudio existente).
- [ ] MMII abre (HC con estudio existente).

## 6) Estudios (PDF)
- [ ] Ecocardiograma PDF imprime y contiene datos del estudio.
- [ ] Ecostress PDF imprime y contiene datos del estudio.
- [ ] Carotidas PDF imprime y contiene textos descriptivos (no codigos).
- [ ] MMII PDF imprime y contiene datos del estudio.

## 7) Consistencia visual
- [ ] Un solo enfoque visual (predominio omar-codex).
- [ ] Sin estilos duplicados en la misma pantalla.

## 8) Seguridad / Config
- [ ] DISABLE_CSRF=1 aplicado solo en entorno de pruebas.
- [ ] Validadores de password vacios (segun regla actual).

## 9) Idempotencia / regresiones
- [ ] Idempotencia verificada con HC 7544 (no duplica visitas).
- [ ] No hay errores 500 en consola / logs.

## 10) Extras
- [ ] PDFs abren en nueva pestaña.
- [ ] Rutas legacy redirigen o estan removidas.

