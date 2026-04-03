# UI BASE (templates comunes)

## Ubicacion
- Base template: `/home/eze/omar/hhcc/main/templates/base.html`
- Header: `/home/eze/omar/hhcc/main/templates/components/header.html`
- Static CSS: `/home/eze/omar/hhcc/main/static/main/css/style.css`
- JS header: `/home/eze/omar/hhcc/main/static/main/js/components/header.js`

## Base template (base.html)
- Usa Tailwind CDN y Alpine CDN.
- Incluye `style.css` local.
- Estructura:
  - Header fijo con menu.
  - `<main>` con `container-content`.
- Bloques: `title`, `extra_css`, `content`, `extra_js`.

## Header (header.html)
- Logo `main/images/logo.png`.
- Titulo: "Dr. Omar Prieto / Cardiología Integral".
- Boton logout con `id="logout-button"`.
- Menu principal:
  - Inicio
  - Pacientes (Buscar/Nuevo)
  - Historias (Buscar + accesos h1/h2/h3)
  - Ordenes (Ordenes Medicas / Solicitudes)
- Breadcrumbs via `breadcrumbs` context.

## Observaciones de integracion
- Estilos y layout base deben alinearse con `/home/eze/omar-codex` (mas nuevo).
- El header es el punto de acople visual comun.
- Regla UI global: **breadcrumbs se eliminan en todo el sistema**.

## CSS (style.css)
- Contiene estilos del header/menu, breadcrumbs y utilitarios extraidos de templates.
- Incluye estilos para `.current-path` y `.breadcrumb-*` (a eliminar por regla).
- Usa `body` con fuente `Segoe UI` y fondo `#f8f9fa`.
- Contiene estilos de historiales (checkbox custom, grids).

## JS (header.js)
- Maneja apertura/cierre de submenus.
- Cierra menus al click fuera.
- Soporta teclado (Enter/Escape).
- Logout redirige a `/logout/`.
