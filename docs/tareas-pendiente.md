
---

## `docs/tareas-pendientes.md` (en clave “equipo de diagnóstico”)

```markdown
# Tareas pendientes (backlog técnico)

Lista de tareas a abordar en el Emulador IPMS como equipo de diagnóstico.

## 1. Protocolo y captura

- [ ] Confirmar protocolo exacto IPMS ↔ lectores (OSDP u otro).
- [ ] Capturar trazas reales en campo o banco de pruebas.
- [ ] Documentar en qué tramas se ven:
  - Eventos de autenticación.
  - Errores.
  - Estados relevantes.

## 2. Módulo RS-485

- [ ] Implementar passthru estable.
- [ ] Implementar modo “sniffer” si es viable.
- [ ] Añadir estadística de errores de comunicación.
- [ ] Integrar con logs (formato JSONL o similar).

## 3. Escenarios de diagnóstico

- [ ] Definir un listado inicial de escenarios:
  - Captura passthru.
  - Emulación básica lado IPMS.
  - Emulación básica lado lector.
  - Prueba YubiKey.
- [ ] Implementar cada escenario como módulo claramente separado.
- [ ] Integrar los escenarios con Node-RED (inicio, parámetros, parada).

## 4. Omnikey + YubiKey

- [ ] Elegir librería PC/SC para Python.
- [ ] Hacer pruebas de conexión básica.
- [ ] Definir las APDUs necesarias para:
  - Verificación de PIN.
  - Lectura de certificado.
  - Challenge/response.
- [ ] Documentar todo en un documento específico (`docs/apdu-yubikey.md` cuando exista).
- [ ] Integrar con el sistema de logs.

## 5. Logs

- [ ] Fijar formato final de logs (campos obligatorios).
- [ ] Implementar rotación.
- [ ] Añadir opción en el dashboard para marcar sesiones de diagnóstico.
- [ ] Probar extracción de logs desde la SD y lectura offline.

## 6. Dashboard Node-RED

- [ ] Crear flujo mínimo de estado + eventos.
- [ ] Añadir control de escenarios de prueba.
- [ ] Añadir pestaña específica para Omnikey/YubiKey.
- [ ] Diseñar indicadores claros para errores y modos.

## 7. LEDs y buzzer

- [ ] Definir tabla de significados de LEDs.
- [ ] Implementar capa de abstracción de indicadores.
- [ ] Probar los patrones de buzzer en distintos estados.

## 8. Seguridad y actualización

- [ ] Definir credenciales de acceso al dashboard.
- [ ] Definir mecanismo de actualización (script de reinstalación).
- [ ] Documentar el procedimiento de actualización para técnicos.
- [ ] Valorar uso del chip criptográfico para proteger datos sensibles.

## 9. Documentación

- [ ] Completar este conjunto de documentos una vez se concreten:
  - Modelo de Raspberry.
  - Esquemas de la placa base.
  - Protocolos exactos.
- [ ] Añadir diagramas en `docs/arquitectura.md` y `docs/flujo-pruebas.md`.

## Sesión 2025-11-22 – Resumen de trabajo

- Aclarado el alcance del proyecto: el Emulador IPMS es una herramienta de diagnóstico para barcos, no un producto permanente ni parte fija del sistema IPMS.
- Definida la estructura lógica del repositorio (src, tests, docs, etc.) y la organización de la documentación.
- Redactados los documentos base:
  - Arquitectura general del equipo de diagnóstico.
  - Flujos de uso (captura, emulación, pruebas con YubiKey).
  - Decisiones técnicas iniciales.
  - Descripción del hardware y topologías de conexión.
  - Plan general de logs y dashboard en Node-RED.
  - Backlog técnico con tareas pendientes.
- Diseñada una configuración de Codex para mantener el código, la documentación y el control de versiones ordenados y consistentes (AGENTS global, AGENTS por repo, config.toml).
