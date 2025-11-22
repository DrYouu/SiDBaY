
---

## `docs/arquitectura.md`

```markdown
# Arquitectura del Emulador IPMS (equipo de diagnóstico)

Este documento describe la arquitectura del equipo de diagnóstico Emulador IPMS.  
El objetivo es dejar claro qué piezas hay, cómo se conectan y qué hace cada una durante las pruebas.

## 1. Vista general

- El Emulador IPMS es una **placa intermedia de diagnóstico** basada en una Raspberry Pi y una placa base específica.
- Se conecta entre:
  - El sistema IPMS original (controladoras/placas del barco).
  - Los lectores o dispositivos de campo.
- Puede funcionar en dos entornos:
  - **En barco**, pinchado en la línea real, para diagnóstico in situ.
  - **En banco de pruebas**, conectado a hardware de pruebas que simula el barco.

Roles principales:

1. **Passthru de diagnóstico**  
   Reenvía el tráfico entre la electrónica IPMS y los lectores, registrándolo en la SD sin alterar la lógica original.

2. **Emulación**  
   Puede emular el comportamiento de alguna de las partes (controladora o lector), para reproducir fallos y escenarios sin depender de todo el sistema.

3. **Pruebas avanzadas**  
   Permite añadir flujos de prueba extra: por ejemplo, probar una YubiKey, validar certificados, simular coacción, etc., sin tocar el software original del barco.

## 2. Componentes hardware

### 2.1. Electrónica IPMS original

- Controladoras y módulos que ya existen en el barco.
- Se conectan al Emulador IPMS a través de uno de los puertos RS-485 de la placa de diagnóstico.
- No se modifican ni se flashean; la herramienta solo observa o emula.

### 2.2. Lectores y dispositivos de campo

- Lectores de tarjetas/contactless, teclados, etc. del sistema original.
- Conectados al Emulador IPMS mediante el segundo puerto RS-485.
- En modo diagnóstico, pueden seguir hablando con la controladora real a través del equipo de diagnóstico.

### 2.3. Placa de diagnóstico (Raspberry Pi + placa base)

Elementos:

- Raspberry Pi (modelo a definir).
- Placa base con:
  - Doble interfaz RS-485.
  - 12 LEDs de estado.
  - Buzzer.
  - RTC.
  - Chip criptográfico.
  - SD dedicada a logs.

Funciones:

- Capturar tráfico de la línea.
- Reenviar tráfico (passthru).
- Ejecutar servicios de diagnóstico en Raspberry (Python).
- Ejecutar Node-RED y servir el dashboard.
- Gestionar LEDs y buzzer como indicadores de estados de prueba.

### 2.4. Omnikey + YubiKey (opcional en pruebas)

- Lector Omnikey conectado por USB a la Raspberry Pi.
- YubiKey insertada en el lector.
- Uso típico:
  - Probar flujos de PIN + certificado.
  - Extraer certificados e identificadores para meter en logs.
  - Testear challenge/response y registrar el resultado.

### 2.5. Dashboard Node-RED

- Flujo Node-RED ejecutándose en la Raspberry Pi.
- Ofrece:
  - Vista de estados (conexión, modo, errores).
  - Listado de eventos y logs recientes.
  - Controles para lanzar o parar escenarios de prueba.
  - Interfaz para introducir PIN cuando se hacen pruebas con YubiKey.

## 3. Módulos lógicos de software

### 3.1. Módulo de enlace RS-485

Responsabilidades:

- Inicializar ambos buses RS-485:
  - Bus IPMS ↔ Emulador.
  - Bus Emulador ↔ lectores.
- Modos de funcionamiento:
  - **Sniffer pasivo** (cuando técnicamente sea posible).
  - **Passthru** (reenviar en ambas direcciones).
  - **Emulación** (el Emulador se comporta como uno de los extremos).

- Registro opcional de tráfico en formato útil para análisis (logs estructurados).

### 3.2. Módulo de escenarios de prueba

Responsabilidades:

- Definir “escenarios de diagnóstico” concretos:
  - Captura simple de eventos en una franja de tiempo.
  - Reproducción de un fallo observado (por ejemplo, ciertas secuencias de tramas).
  - Prueba de YubiKey (flujo PIN + certificado).
- Adaptar la lógica de la herramienta según el escenario activo:
  - Decidir si se está en modo observación pura o emulación parcial.
  - Activar o no la lógica de Omnikey/YubiKey.

### 3.3. Módulo Omnikey/YubiKey (PC/SC)

Responsabilidades:

- Hablar con el lector Omnikey vía PC/SC.
- Ejecutar APDUs contra la YubiKey:
  - Solicitud de PIN.
  - Verificación de PIN.
  - Obtención de certificado o identificador.
  - Challenge/response.
- Entregar a los módulos de escenario:
  - Resultado (OK / fallo / bloqueo / coacción si se define).
  - Datos relevantes (hash, certificado, identificador).

### 3.4. Módulo de logs

Responsabilidades:

- Escribir logs en la SD de la placa.
- Formato estructurado (por ejemplo JSONL):
  - Timestamp (RTC).
  - Identificador de barco (si se configura).
  - Identificador de línea/lector.
  - Tipo de evento (tráfico, escenario, YubiKey, error…).
  - Detalles (UID, certificado, resultado del challenge, etc.).
- Ofrecer a Node-RED:
  - Lectura de eventos recientes.
  - Posibilidad de exportar segmentos de log.

### 3.5. Módulo de indicadores (LEDs y buzzer)

Responsabilidades:

- Abstraer el uso de los 12 LEDs y del buzzer:
  - Indicar modo actual (passthru, emulación, captura, error).
  - Indicar estado de Omnikey/YubiKey.
  - Mostrar de un vistazo si el equipo está en un escenario de prueba concreto.
- Evitar que cada módulo toque GPIO directamente; centralizar la lógica.

### 3.6. Módulo de integración con Node-RED

Responsabilidades:

- Proporcionar a Node-RED los datos que necesita:
  - Estados, eventos, resultados de escenarios.
- Recibir desde Node-RED acciones:
  - Arrancar/parar escenarios.
  - Solicitudes de lectura de log.
  - Parámetros de prueba (por ejemplo, qué tipo de certificado validar).

## 4. Topologías de uso

### 4.1. Uso en barco (diagnóstico in situ)

- El equipo se pincha en la línea entre IPMS y lectores, sin sustituir al sistema original.
- El técnico define:
  - Si solo quiere observar tráfico.
  - Si quiere emular parte de la línea.
- Los resultados se ven en Node-RED y se guardan en SD.

### 4.2. Uso en banco de pruebas

- La Raspberry Pi y la placa se conectan a hardware de laboratorio:
  - Simulador de IPMS.
  - Simulador de lectores.
- Permite reproducir errores sin depender del barco.
- Escenarios se pueden repetir con las mismas condiciones.

## 5. Diagrama (pendiente)

> Queda pendiente añadir diagramas de bloques y de secuencia específicos cuando se concreten los detalles de protocolo y cableado final.
