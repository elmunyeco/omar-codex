import json

def menu_context(request):
    """
    Añade variables de contexto relacionadas con la navegación y el menú.
    Esto estará disponible en todos los templates automáticamente.
    """
    # Determinar la sección activa basada en la URL
    active_section = ''
    path = request.path or '/'
    normalized = path.strip('/')
    parts = [p for p in normalized.split('/') if p]

    if '/pacientes' in path:
        active_section = 'pacientes'
    elif '/historias' in path or '/historial_medico' in path:
        active_section = 'historias'
    elif '/ordenes' in path:
        active_section = 'ordenes'
    elif path == '/' or path == '/index/' or path == '/index.html':
        active_section = 'inicio'

    # Configurar breadcrumbs predeterminados
    breadcrumbs = [{"label": "Inicio", "url": "/"}]

    if active_section == 'pacientes':
        breadcrumbs.append({"label": "Pacientes", "url": "/pacientes/"})
        if 'pacientes/crear' in path:
            breadcrumbs.append({"label": "Nuevo Paciente", "url": None})
        elif 'pacientes/' in path and len(parts) >= 2 and parts[0] == 'pacientes':
            breadcrumbs.append({"label": f"Paciente {parts[1]}", "url": None})
        elif 'listar_buscar_pacientes' in path or 'buscar' in path:
            breadcrumbs.append({"label": "Buscar Pacientes", "url": None})

    elif active_section == 'historias':
        breadcrumbs.append({"label": "Historias", "url": "/historias/"})
        if parts and parts[0] == 'historias' and len(parts) >= 2 and parts[1].isdigit():
            historia_id = parts[1]
            breadcrumbs.append(
                {"label": f"Historia {historia_id}", "url": f"/historial_medico/{historia_id}/"}
            )
            if len(parts) >= 3 and parts[2] == 'estudios':
                breadcrumbs.append(
                    {"label": "Estudios", "url": f"/historias/{historia_id}/estudios/"}
                )
                if len(parts) >= 4 and parts[3] == 'nuevo':
                    breadcrumbs.append({"label": "Nuevo estudio", "url": None})
        elif parts and parts[0] == 'historial_medico' and len(parts) >= 2 and parts[1].isdigit():
            breadcrumbs.append({"label": f"Historia {parts[1]}", "url": None})
        elif 'listar_buscar_historias' in path or 'buscar' in path:
            breadcrumbs.append({"label": "Buscar Historias", "url": None})

    elif active_section == 'ordenes':
        breadcrumbs.append({"label": "Órdenes", "url": "/ordenes/"})
        if 'ordenes_medicas' in path:
            breadcrumbs.append({"label": "Órdenes Médicas", "url": None})
        elif 'ordenes_pedicas' in path:
            breadcrumbs.append({"label": "Solicitudes", "url": None})

    return {
        'active_section': active_section,
        'breadcrumbs': breadcrumbs,
        'breadcrumbs_json': json.dumps(breadcrumbs),
    }
