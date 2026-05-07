# Roadmap técnico

## Fase 1 — Validación funcional local
- Estado: **completado parcialmente**.
- Objetivo: asegurar flujo base policy/link/lab.
- Tareas: pruebas unitarias e integración local.
- Criterio de éxito: estabilidad de suite y reportes trazables.
- Riesgo: cobertura incompleta de edge cases.

## Fase 2 — Pruebas negativas y fail-safe
- Estado: **completado parcialmente**.
- Objetivo: validar bloqueo/rechazo en fallos.
- Tareas: downgrade/replay/desync/fragmentación.
- Criterio de éxito: no degradación silenciosa.
- Riesgo: falsos positivos por simulación.

## Fase 3 — Máxima seguridad en redes failure
- Estado: **en curso**.
- Objetivo: endurecer `MAX_SECURITY` bajo degradación.
- Tareas: perfiles lora_failure/lora_extreme y consistencia de key switch.
- Criterio de éxito: bloqueo seguro o envío seguro, sin silent downgrade.
- Riesgo: trade-off entrega vs seguridad.

## Fase 4 — Integración ML-KEM real
- Estado: **pendiente**.
- Objetivo: reemplazar mocks PQC en KEM.
- Tareas: integrar lib, pruebas vectoriales, hardening de errores.
- Criterio de éxito: interop y verificación criptográfica reproducible.
- Riesgo: costo CPU/MTU/latencia.

## Fase 5 — Integración ML-DSA real
- Estado: **pendiente/opcional**.
- Objetivo: evaluar identidad híbrida real.
- Tareas: diseño de compatibilidad y tamaño de firmas.
- Criterio de éxito: firma verificable sin romper ecosistema.
- Riesgo: overhead elevado.

## Fase 6 — Pruebas `tc/netem` reales
- Estado: **pendiente**.
- Objetivo: validar degradaciones kernel-level.
- Tareas: perfiles reproducibles, métricas de jitter/loss/latencia.
- Criterio de éxito: coherencia con resultados de harness.
- Riesgo: variabilidad de entorno.

## Fase 7 — Pruebas hardware LoRa
- Estado: **pendiente**.
- Objetivo: validar en RF real.
- Tareas: campañas de campo y laboratorio RF.
- Criterio de éxito: comportamiento estable bajo restricciones reales.
- Riesgo: alta variabilidad física.

## Fase 8 — Auditoría de seguridad
- Estado: **pendiente**.
- Objetivo: revisión independiente.
- Tareas: threat model, revisión protocolo, pruebas adversarias.
- Criterio de éxito: hallazgos críticos mitigados.
- Riesgo: costos/tiempo.

## Fase 9 — Hardening para red privada
- Estado: **pendiente**.
- Objetivo: madurez operacional.
- Tareas: observabilidad, controles operativos, respuesta a incidentes.
- Criterio de éxito: operación estable y gobernable.
- Riesgo: deuda técnica acumulada.
