# Changelog

## [0.1.0] - 2025-11-22

### Añadido
- Definida la estructura base del repositorio (`src/`, `tests/`, `docs/`, `.vscode/`, `README.md`, `CHANGELOG.md`, `.gitignore`).
- Redactada la documentación inicial del proyecto como **equipo de diagnóstico para sistemas IPMS en barcos**, aclarando que es una herramienta de trabajo puntual y no un elemento permanente de la instalación.
- Creado el esquema de documentación en `docs/`:
  - `arquitectura.md`: arquitectura general del Emulador IPMS como herramienta de diagnóstico.
  - `flujo-pruebas.md`: flujos de captura, emulación y pruebas con Omnikey + YubiKey.
  - `decisiones-tecnicas.md`: decisiones técnicas iniciales (rol de la herramienta, plataforma, logs, uso de Omnikey/YubiKey, etc.).
  - `hardware.md`: componentes hardware principales y topologías de uso (barco y laboratorio).
  - `logs-y-dashboard.md`: planteamiento de logs en SD y dashboard Node-RED.
  - `tareas-pendientes.md`: backlog técnico inicial.
- Definida la configuración conceptual de Codex:
  - `~/.codex/AGENTS.md` con reglas globales de estilo, organización y uso de Git.
  - `AGENTS.md` en el repo para las normas específicas del Emulador IPMS.
  - `config.toml` para fijar modelo, sandbox y política de aprobación de comandos.

### Pendiente
- Implementar el módulo RS-485 de passthru y captura.
- Crear los primeros flujos de Node-RED y dashboard real.
- Probar Omnikey + YubiKey vía PC/SC en la Raspberry Pi.
- Completar detalles de hardware (modelo exacto de Pi, placa base, esquemas).
