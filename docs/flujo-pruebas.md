# Flujos de pruebas y diagnóstico

Este documento describe los flujos principales de uso del Emulador IPMS como herramienta de diagnóstico.  
No describe el uso normal del sistema original, sino cómo se utiliza el equipo de trabajo para observar y probar ese sistema.

## 1. Flujo básico de captura en modo passthru

Objetivo: obtener una traza lo más fiel posible del comportamiento real, sin intervenir en la lógica del sistema.

1. El técnico conecta el Emulador IPMS:
   - Entre la electrónica IPMS y los lectores (en barco).
   - O a un banco de pruebas que simule ambas partes.
2. Selecciona en Node-RED el **escenario “Captura passthru”**.
3. El módulo RS-485 entra en modo passthru:
   - Reenvía todo el tráfico en ambas direcciones.
   - Registra las tramas en los logs (según configuración).
4. El sistema original funciona como siempre.
5. El técnico:
   - Observa el tráfico en el dashboard.
   - Marca en el tiempo los eventos de interés (por ejemplo, un fallo).
6. Al finalizar:
   - Se cierra el escenario.
   - Se conserva el archivo de log para análisis posterior.

## 2. Flujo de emulación básica

Objetivo: reproducir en laboratorio un problema observado en barco.

1. Se carga en el equipo:
   - La configuración de IPMS simulada.
   - Los parámetros relevantes del escenario (tiempos, respuestas esperadas, etc.).
2. El técnico selecciona en Node-RED el **escenario “Emulación básica”**:
   - El Emulador se comporta, por ejemplo, como la controladora IPMS frente a un lector real, o viceversa.
3. El módulo RS-485:
   - Deja de ser passthru.
   - Genera o responde tramas simulando la parte deseada.
4. Se reproduce el problema:
   - Repitiendo patrones de tráfico.
   - Cambiando condiciones para ver cuándo aparece o desaparece el fallo.
5. Los resultados se registran en logs, incluyendo:
   - Parámetros del escenario.
   - Tramas enviadas y recibidas.
   - Comentarios del técnico (si se añade interfaz para ello).

## 3. Flujo de prueba con Omnikey + YubiKey

Objetivo: validar flujos de PIN/certificado en una YubiKey y registrar el resultado dentro de un escenario de diagnóstico.

1. El técnico conecta Omnikey + YubiKey al Emulador IPMS.
2. En Node-RED selecciona el **escenario “Prueba YubiKey”**.
3. El sistema:
   - Comprueba si el lector Omnikey y la YubiKey están disponibles.
   - Muestra en el dashboard el estado (OK / no disponible / error).
4. El técnico lanza una prueba:
   - Por ejemplo: “verificar PIN + obtener certificado”.
   - Node-RED, a través del módulo de pruebas, recoge el PIN (dashboard) o simula uno.
5. El módulo PC/SC:
   - Envía las APDUs a la YubiKey.
   - Recibe el resultado (PIN correcto/incorrecto, certificado, challenge/response, etc.).
6. El resultado se registra en logs:
   - Timestamp.
   - Tipo de prueba.
   - Resultado (`OK`, `PIN_FALLO`, `BLOQUEO`, `COACCION` si se define).
   - Certificado o identificador (según se decida).
   - Hash o resultado del challenge.

Este flujo NO es el login real de usuarios del barco; es una prueba controlada para validar y documentar cómo se comporta la YubiKey en ese entorno.

## 4. Flujo mixto: captura + prueba avanzada

Objetivo: correlacionar el comportamiento del sistema real con una prueba avanzada.

Ejemplo:

1. El equipo está en **escenario “Captura passthru”** en un barco.
2. Se detecta un comportamiento sospechoso en la línea.
3. El técnico:
   - Marca el momento en el dashboard.
   - Lanza un escenario de prueba YubiKey asociado a ese contexto (misma instalación, mismo barco).
4. Se registran en el log:
   - El evento de la línea.
   - El resultado de la prueba avanzada.
5. Posteriormente, se correlacionan ambos para análisis.

## 5. Escenarios especiales y errores

### 5.1. YubiKey u Omnikey no disponibles

- El escenario de prueba YubiKey:
  - Debe detectar la ausencia.
  - No debe colgar ni bloquear el resto de la herramienta.
- Acción:
  - Registrar un evento de error en el log.
  - Mostrar claramente en Node-RED que la prueba no se ha podido ejecutar.

### 5.2. Problemas en RS-485 durante diagnóstico

- Si hay errores de comunicación:
  - Registrar los eventos y estadísticas de error.
  - Mostrar en el dashboard indicadores claros (LEDs, buzzer y panel).
- La política de cómo actuar (seguir, parar, reiniciar) se definirá en `docs/decisiones-tecnicas.md`.

## 6. Puntos pendientes de definir

- Formato detallado de cada evento de log asociado a estos flujos.
- Convenciones de nombres para escenarios de prueba.
- Políticas de seguridad (quién puede ejecutar qué escenarios y desde dónde).
