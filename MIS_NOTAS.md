 ## Comparación completa

  1) Pacientes (editar)
  Legacy (scrap_legacy/crawl_7544/docs/legacy_intranet-cardioprieto_4.md):

  - id, tipoDoc, numDoc, nombre, apellido, fechaNac, sexo, email, direccion, localidad, obraSocial, plan, afiliado, telefono, celular, profesion,
    referente

  Local (pacientes_edit_*.html en Scrap_cardioprietohc/data/raw/local_crawl_8081/):

  - idTipoDoc, numDoc, nombre, apellido, fechaNac, sexo, mail, direccion, localidad, obraSocial, plan, afiliado, telefono, celular, profesion,
    referente + csrfmiddlewaretoken

  Diferencias concretas:

  - email (legacy) vs mail (local)
  - tipoDoc (legacy) vs idTipoDoc (local)
  - id hidden en legacy, no en local (se usa id en URL)
  - csrfmiddlewaretoken solo en local (Django)

  2) Historia clínica / HC (verHClinica)
  Legacy (legacy_intranet-cardioprieto_verHClinica.md):

  - Diagnóstico: enfermedades[] (25), idHC
  - Comentarios: comentario, tipoComentario, proteger, idHC
  - Signos vitales: peso, colesterol, glucemia, presionSistolica, presionDiastolica, idHC
  - Enviar indicaciones: mail

  Local (/historial_medico/<id>/ + main/views.py):

  - UI con inputs sin name, se guarda vía JSON:
      - signos_vitales: presion_sistolica, presion_diastolica, peso, glucemia, colesterol
      - condiciones: lista de ids (1..25)
      - comentarios: texto
  - Endpoints:
      - POST /api/historia/<id>/guardar/
        Mapea a guardar_historia en hhcc/main/views.py
      - POST /eliminar-comentario/

  Diferencias concretas:

  - Legacy separa endpoints por módulo (diagnóstico, comentario, signos, mail).
    Local unifica en guardar_historia.
  - Legacy tiene tipoComentario y proteger; no existe en local.
  - Legacy usa presionSistolica/Diastolica; local usa presion_sistolica/diastolica (snake_case).
  - Legacy tiene mail en HC (enviar indicaciones). Local no tiene envío por email desde HC.
  - Local agrega csrfmiddlewaretoken y usa JSON.

  3) Indicaciones
  Legacy:

  - POST /hClinica/enviarIndicaciones/<id> con mail

  Local (hhcc/main/templates/indicaciones/lista.html):

  - Indicaciones y comentarios se gestionan en pantalla aparte:
      - POST /historia/<id>/indicaciones/comentario/ (guardar comentario)
      - POST /indicaciones/<id>/eliminar/
  - No hay envío por mail.

  ———

  ## Conclusiones principales (gap list)

  1. Falta equivalente directo a “Enviar indicaciones por mail” (legacy) en local.
  2. tipoComentario y proteger no existen en local.
  3. email vs mail en paciente: hay diferencia de naming.
  4. tipoDoc vs idTipoDoc en paciente: naming distinto.
  5. HC local usa JSON + endpoints unificados, no forms tradicionales.
