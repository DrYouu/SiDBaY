# Emulador IPMS – Equipo de diagnóstico para sistemas de acceso en barcos

Este proyecto es un **equipo de diagnóstico y emulación** para sistemas de acceso IPMS instalados en barcos.  
No es un producto comercial ni un componente permanente de la instalación: es una herramienta de trabajo para técnicos, diseñada para un proyecto concreto.

El dispositivo se conecta en la línea entre la electrónica del sistema IPMS original y sus lectores, o en un banco de pruebas, y permite:

- Observar y registrar el tráfico de la línea (RS-485 / OSDP u otro protocolo que use el sistema).
- Emular comportamientos de la placa IPMS o de los lectores para reproducir fallos o escenarios.
- Probar e integrar mecanismos avanzados de autenticación (por ejemplo, verificación de certificados en una YubiKey a través de un lector Omnikey).
- Generar logs estructurados en una tarjeta SD de la propia placa.
- Visualizar estados y resultados en un dashboard Node-RED.
- Usar los LEDs y el buzzer de la placa como indicadores de estado durante las pruebas.

Todo el diseño es **cerrado, privado y específico** para este proyecto. La API del sistema original no se usa de forma completa, solo lo estrictamente necesario para diagnóstico y emulación.

## Objetivos

- Disponer de una herramienta portátil para:
  - Diagnosticar problemas de comunicación y autenticación en sistemas IPMS de barcos.
  - Registrar trazas completas de eventos para análisis posterior.
  - Validar nuevas ideas de seguridad (p.ej. uso de YubiKey) sin tocar el software original.
- Mantener un flujo de trabajo reproducible:
  - Misma estructura de logs.
  - Mismas pantallas de Node-RED.
  - Procedimientos claros de prueba.

## Alcance

- El Emulador IPMS:
  - No sustituye al sistema original.
  - No se queda instalado de forma permanente en el barco.
  - Se utiliza por personal técnico, en modo diagnóstico, pruebas o auditoría.

## Estado actual (2025-11-22)

A nivel de diseño y documentación:

- [x] Definido el rol del Emulador IPMS como **equipo de diagnóstico** específico para sistemas IPMS en barcos.
- [x] Establecida la estructura base del repositorio (código, tests, docs, configuración de editor).
- [x] Redactada la documentación inicial:
  - Arquitectura del sistema.
  - Flujos de pruebas y escenarios de diagnóstico.
  - Decisiones técnicas iniciales.
  - Esquema de hardware y topologías de uso.
  - Plan de logs y dashboard.
  - Backlog técnico.
- [x] Propuesta de configuración para Codex / GPT en VS Code:
  - Reglas globales de estilo y organización.
  - Reglas específicas para este repositorio.
  - Configuración de sandbox y modelo.

A nivel de implementación:

- [ ] Módulo RS-485 en Raspberry Pi (passthru, sniffer, emulación).
- [ ] Flujos Node-RED mínimos (estado + eventos).
- [ ] Integración PC/SC con Omnikey + YubiKey en la Raspberry Pi.
- [ ] Uso real de LEDs y buzzer según tabla de estados.
- [ ] Procedimiento de despliegue y actualización del equipo de diagnóstico.

## Arquitectura (resumen)

Componentes principales:

- Electrónica IPMS original (controladora y/o placas del sistema del barco).
- Lectores y dispositivos de campo del sistema original.
- Placa intermedia de diagnóstico:
  - Raspberry Pi.
  - Doble interfaz RS-485.
  - SD para logs.
  - 12 LEDs, buzzer, RTC, chip criptográfico.
- Lector Omnikey + YubiKey (para pruebas de certificados/PIN).
- Dashboard Node-RED para control y visualización.

Más detalle en:

- `docs/arquitectura.md`
- `docs/flujo-pruebas.md`
- `docs/hardware.md`
- `docs/logs-y-dashboard.md`

## Requisitos (trabajo en curso)

- Raspberry Pi (modelo a concretar).
- Placa base con:
  - Doble RS-485.
  - LED x12, buzzer, RTC, chip criptográfico, SD.
- Lector Omnikey compatible PC/SC.
- YubiKey compatible con el tipo de APDU/certificados que se quieran probar.
- Node-RED instalado en la Raspberry Pi.
- Python + librerías para:
  - Serie/RS-485.
  - PC/SC.
  - Generación de logs.

## Estructura del repositorio

```text
src/
  rpi/              Código Python/servicios de la Raspberry Pi
  nodered/          Flujos y recursos de Node-RED
tests/              Scripts de prueba y validación
docs/
  arquitectura.md
  flujo-pruebas.md
  decisiones-tecnicas.md
  hardware.md
  logs-y-dashboard.md
  tareas-pendientes.md
README.md
CHANGELOG.md
.vscode/
.gitignore
