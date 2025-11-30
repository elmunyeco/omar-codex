# Proyecto: Reconstrucción de Sistema de Historias Clínicas Dr. Omar Prieto

## Descripción General del Proyecto

Este proyecto tiene como objetivo rehacer completamente el sistema de historias clínicas online del Dr. Omar Prieto. El sistema original está actualmente en línea y cuento con acceso al mismo (usuario: `omar`, contraseña: `Corbis5`). El Dr. Prieto me ha encargado esta tarea debido a prácticas comerciales desleales del desarrollador original, quien mantiene el sistema "cautivo".

Llevo aproximadamente 5 años (incluyendo el período de pandemia) intentando finalizar este proyecto y he tenido dificultades para encontrar el tiempo necesario.

## Recursos Disponibles

*   **Acceso al Sistema Original:** Usuario: `omar`, Contraseña: `Corbis5`. Se puede acceder a toda la información visible a través de este usuario.
*   **Dump de Base de Datos:** Se cuenta con un dump de la base de datos del sistema original.
*   **Código Existente:** El proyecto ya contiene el código que he estado desarrollando hasta el momento.

## Tecnologías Utilizadas

*   **Framework:** Django
*   **Frontend:** Tailwind CSS y Alpine.js (reemplazando Bootstrap y jQuery)

## Metodología y Restricciones Operativas para Gemini

1.  **Crawling y Comparación:** Es ABSOLUTAMENTE NECESARIO realizar crawling del sistema online existente. Esta información debe compararse con el código ya escrito y con la base de datos existente para identificar funcionalidades faltantes o diferencias.
2.  **Homogeneidad:** Cualquier avance o nueva implementación debe seguir de manera homogénea las decisiones de diseño y tecnológicas ya tomadas (Django, Tailwind CSS, Alpine.js).
3.  **Consulta y Colaboración:** Cualquier otra decisión o implementación se consultará entre el modelo Gemini y yo. NO habrá modo YOLO (You Only Live Once); no se tomarán decisiones importantes sin mi validación.
4.  **Restricción de Directorio:** El modelo Gemini NO puede salirse del directorio del proyecto a un nivel superior del filesystem.
5.  **Bases de Datos en Docker:** Tanto la base de datos antigua (del dump) como la nueva (del proyecto Django) estarán corriendo en dos contenedores Docker separados. Gemini debe considerar esta configuración.
6.  **Entrega de Código:** Cualquier modificación o avance se entregará en formato de código.
7.  **Checkpoints de Commit:** Una vez que se complete una modificación importante (no en pasos intermedios de desarrollo), se debe realizar un commit en el repositorio del proyecto para marcar un "checkpoint".

## Nota adicional de visualizacion
- Prioridad: reproducir fielmente layouts, posiciones, colores, espaciados y componentes del sistema original antes de tocar lógica/datos.
- No cambiar UI salvo pedido explícito o mejora indiscutible; si faltan assets CSS/JS, obtenerlos primero.
- El scrape se usa para capturar estructura/flujo visual, no solo datos.
