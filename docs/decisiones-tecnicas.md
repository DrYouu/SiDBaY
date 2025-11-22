# Decisiones técnicas

Documento para registrar decisiones técnicas relevantes del Emulador IPMS como equipo de diagnóstico para barcos.

## 1. Rol del sistema: herramienta de diagnóstico, no parte permanente

**Decisión**

El Emulador IPMS se utilizará exclusivamente como herramienta de diagnóstico y pruebas:

- No se instalará de forma permanente en barcos.
- No sustituye a ningún componente IPMS original.

**Motivación**

- Evitar dependencia de un equipo de diagnóstico en producción.
- Mantener la instalación original lo más intacta posible.
- Separar claramente responsabilidades:
  - IPMS: control de acceso del barco.
  - Emulador IPMS: diagnóstico y pruebas puntuales.

## 2. Plataforma principal: Raspberry Pi + placa base específica

*(igual que antes, pero explícitamente orientado a diagnóstico; mantengo solo lo necesario)*

**Decisión**

Usar Raspberry Pi con una placa base que aporta RS-485, LEDs, buzzer, RTC, chip criptográfico y SD para logs.

**Motivación**

- Flexibilidad y potencia para:
  - Captura de tráfico.
  - Emulación.
  - Node-RED.
  - Pruebas con Omnikey/YubiKey.
- Integración relativamente sencilla con herramientas de diagnóstico (Wireshark, Python, etc.).

## 3. Lenguajes y tecnologías

**Decisión inicial**

- Lógica principal de diagnóstico y pruebas: Python.
- Panel y orquestación visual: Node-RED.

**Motivación**

- Desarrollo rápido.
- Fácil modificación y prueba en campo.
- Ecosistema de librerías para serie, PC/SC y red.

## 4. Logs y SD de la placa

**Decisión**

- Todos los logs de diagnóstico importantes se escriben en la SD de la placa base.
- El técnico puede extraer esa SD para análisis fuera de la instalación.

**Motivación**

- Mantener los datos de diagnóstico independientes del IPMS.
- Poder guardar sesiones completas de pruebas para documentación del trabajo realizado.

## 5. Uso de Omnikey + YubiKey

**Decisión**

Integrar opcionalmente un lector Omnikey con YubiKey como parte de ciertos escenarios de prueba.

**Motivación**

- Validar conceptos de autenticación fuerte.
- Probar certificados, PIN, challenge/response en un entorno real de barco sin tocar el software IPMS.

**Alcance**

- Es una capacidad de diagnóstico / laboratorio, no una exigencia del sistema original.

## 6. Conectividad y actualizaciones

**Decisión preliminar**

- El equipo puede crear una WiFi tipo AP para acceso local del técnico al dashboard.
- Las actualizaciones se harán:
  - Solo cuando se publiquen expresamente.
  - Mediante un script de reinstalación controlado.
- Usuario y contraseña de acceso sencillos pero definidos por configuración (no por defecto inseguros en producción real).

**Motivación**

- Control estricto de cambios (no hay actualizaciones automáticas fuera de control).
- Uso en entornos aislados (barco, laboratorio) sin depender de internet.

## 7. Seguridad y confidencialidad

**Decisión**

- El diseño, los protocolos y los logs de pruebas se consideran información privada del proyecto.
- El acceso al dashboard y a la SD debe estar restringido al equipo técnico autorizado.

Los detalles finos (usuarios, contraseñas, cifrado de logs, uso del chip criptográfico) se completarán cuando se concreten en el desarrollo.
