\# AGENTS.md



\## Convenciones de este repositorio



\- Estructura esperada:

&nbsp; - `src/`: código principal del proyecto.

&nbsp; - `tests/`: pruebas unitarias, de integración o scripts de validación.

&nbsp; - `docs/`: documentación del proyecto.

&nbsp; - `README.md`: descripción general, instalación y uso básico.

&nbsp; - `CHANGELOG.md`: historial de versiones siguiendo SemVer (MAJOR.MINOR.PATCH).

\- Siempre que el comportamiento o la interfaz externa cambien:

&nbsp; - Actualiza `README.md` con la información necesaria para usuarios.

&nbsp; - Añade detalles técnicos en uno o varios archivos dentro de `docs/`.

&nbsp; - Añade una entrada en `CHANGELOG.md` bajo la versión correcta o la sección “Unreleased”.



\## Flujo de trabajo esperado



\- Supón que se trabaja en ramas temáticas:

&nbsp; - `feat/...` para funcionalidades.

&nbsp; - `fix/...` para correcciones.

&nbsp; - `chore/...` para tareas internas.

\- Un cambio lógico = un commit:

&nbsp; - Incluye en el mismo commit código, tests y documentación coherentes entre sí.

\- Al proponer cambios:

&nbsp; - Prioriza primero código en `src/`.

&nbsp; - Si procede, propone tests en `tests/`.

&nbsp; - Acompaña con cambios en `docs/` y `CHANGELOG.md`.



\## Reglas para sugerencias de commits y changelog



\- Mensajes de commit:

&nbsp; - Formato `tipo: descripción breve` (en español, imperativo).

&nbsp; - Usa solo los tipos `feat`, `fix`, `docs`, `chore` salvo que el usuario pida otros.

\- Entradas de `CHANGELOG.md`:

&nbsp; - Agrupa los cambios en viñetas bajo la versión correspondiente.

&nbsp; - Describe siempre:

&nbsp;   - Qué se ha hecho.

&nbsp;   - En qué parte del sistema.

&nbsp;   - Si cambia la interfaz o solo la implementación interna.



\## Cómo debe ayudar Codex en este repositorio



\- Nuevas funcionalidades:

&nbsp; 1. Proponer archivos y cambios en `src/`.

&nbsp; 2. Proponer pruebas mínimas viables en `tests/`.

&nbsp; 3. Indicar qué documentación en `docs/` debería actualizarse o crearse.

&nbsp; 4. Proponer texto para la entrada de `CHANGELOG.md`.

\- Refactors o limpieza:

&nbsp; - Mantener la API pública salvo que el usuario diga explícitamente lo contrario.

&nbsp; - Reducir complejidad, duplicación y código muerto.

&nbsp; - Explicar en el mensaje de commit qué se ha simplificado.

\- Documentación:

&nbsp; - Mantener coherencia terminológica con el resto de los archivos del repo.

&nbsp; - Evitar duplicar información; enlazar o referirse a documentos ya existentes cuando sea posible.



