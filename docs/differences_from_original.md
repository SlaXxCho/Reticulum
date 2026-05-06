# Diferencias con el Reticulum original

Este documento resume **qué cambió** respecto a la base original de Reticulum en este fork de laboratorio.

> Made by **SlaXx**.

## Alcance
- Enfoque en red privada/laboratorio para seguridad adaptativa y validación de escenarios degradados.
- No sustituye la documentación canónica del proyecto original.

## Cambios principales
1. **Perfiles criptográficos adaptativos**
   - `classic`, `hybrid_light`, `hybrid_strong`, `pqc_experimental`.
2. **Policy por mensaje (`security_tag`)**
   - `STANDARD`, `PREFERRED_SECURE`, `MUST_DELIVER`, `MAX_SECURITY`.
3. **Policy Engine**
   - Decisión de envío/bloqueo/upgrade en función de capacidades y mínimos.
4. **Upgrade PQC en Link**
   - Flujo de negociación/upgrade y versionado de clave (`key_version`).
5. **Laboratorio local**
   - `lab_local/run_lab.py`, perfiles de red y reportes reproducibles.
6. **Validación negativa**
   - Casos de downgrade, replay, desync y fallos de fragmentación.

## Diferencia clave de postura
- **Reticulum original**: referencia de protocolo y manual canónico.
- **Este fork**: extensión experimental para pruebas y documentación de seguridad adaptativa.

## Estado de validación
- Comportamiento funcional: **VALIDATED** (según pruebas locales).
- PQC en laboratorio: **SIMULATED / NOT CONCLUSIVE** cuando no hay integración criptográfica real.
- LoRa físico: **NOT CONCLUSIVE** sin hardware real.
