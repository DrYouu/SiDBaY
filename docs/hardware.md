# Hardware del Emulador IPMS (equipo de diagnóstico)

Este documento recoge los elementos hardware relevantes para el equipo de diagnóstico.

## 1. Placa de diagnóstico (Raspberry Pi + placa base)

### 1.1. Raspberry Pi

- Modelo: pendiente (Pi 4, CM, etc.).
- Interfaces que se van a usar:
  - USB: lector Omnikey.
  - Ethernet/WiFi: acceso del técnico (Node-RED).
  - GPIO: conexión con RS-485, LEDs, buzzer, RTC, chip criptográfico, SD (según diseño de la placa base).

### 1.2. Placa base

Características disponibles:

- Doble RS-485:
  - RS-485 A: lado IPMS.
  - RS-485 B: lado lector/dispositivo.
- 12 LEDs.
- Buzzer.
- RTC.
- Chip criptográfico.
- SD para logs (independiente de la SD del sistema de la Pi, si procede).

Uso previsto:

- Permitir conectar el equipo en la línea IPMS sin recablear medio barco.
- Dar feedback visual/sonoro al técnico.
- Mantener la hora precisa para logs con el RTC.
- Aprovechar el chip criptográfico en caso de cifrado de datos sensibles (por definir).

## 2. Conexiones típicas en campo

### 2.1. Modo diagnóstico en barco

```text
[IPMS original] <== RS-485 A ==> [Placa Emulador IPMS] <== RS-485 B ==> [Lector / Dispositivo]
                                 (Raspberry Pi + Node-RED + logs SD)
