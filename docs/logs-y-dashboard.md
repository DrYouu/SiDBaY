
---

## `docs/logs-y-dashboard.md` (ya orientado a diagnóstico, mínimos cambios)

```markdown
# Logs y dashboard en el Emulador IPMS

Este documento explica cómo se registran los datos de diagnóstico y cómo se muestran en Node-RED.

## 1. Logs en SD

### 1.1. Objetivo

- Tener un registro completo y autónomo de:
  - Tráfico entre IPMS y lectores.
  - Escenarios de prueba ejecutados.
  - Resultados de pruebas con Omnikey/YubiKey.
  - Errores de comunicación o de sistema.

### 1.2. Formato (propuesta)

- Archivos de texto en formato JSON Lines (`.jsonl`):
  - Una línea = un evento.
  - Ejemplo:

```json
{
  "ts": "2025-11-22T10:15:30Z",
  "boat_id": "BARCO-001",
  "line_id": "LINEA-01",
  "event": "SCENARIO_RESULT",
  "scenario": "PRUEBA_YUBIKEY",
  "result": "OK",
  "details": {
    "uid": "04AABBCCDDEE",
    "cert_id": "123456",
    "challenge_hash": "abcd..."
  }
}
