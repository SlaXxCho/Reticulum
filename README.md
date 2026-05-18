# Reticulum Adaptativo (Fork de laboratorio)

> **Made by SlaXx**

## Estado del proyecto
Este repositorio es una variante de Reticulum enfocada en **investigación y laboratorio** para seguridad adaptativa.

- No está orientado todavía a producción.
- Parte de la criptografía PQC puede estar en modo **SIMULATED / NOT CONCLUSIVE**.

---

## Resumen rápido de qué cambia frente al Reticulum normal

En el Reticulum base, la seguridad criptográfica y el flujo de enlace son clásicos y uniformes.  
En este fork se añade una capa de decisión adaptativa:

1. **Perfiles criptográficos configurables**.
2. **`security_tag` por mensaje** para ajustar política según criticidad.
3. **Policy Engine** para decidir enviar, bloquear o exigir upgrade.
4. **Upgrade PQC/híbrido dentro de Link** (sin romper de inicio el flujo clásico base).
5. **Versionado de clave (`key_version`)** para cambios de clave coordinados.
6. **Controles anti-downgrade y anti-replay** en la capa de control de seguridad.
7. **Laboratorio local reproducible** con simulación de redes degradadas tipo LoRa.

Documento comparativo detallado: [Diferencias con Reticulum original](docs/differences_from_original.md).

---

## Dónde están los cambios (mapa rápido)

- Perfiles y selección: [`RNS/crypto_profiles.py`](RNS/crypto_profiles.py)
- Política de decisión: [`RNS/security_policy.py`](RNS/security_policy.py)
- Control de upgrade PQC: [`RNS/pqc_upgrade.py`](RNS/pqc_upgrade.py)
- Integración en enlace: [`RNS/Link.py`](RNS/Link.py)
- Laboratorio local: [`lab_local/`](lab_local)
- Pruebas: [`tests/`](tests)
- Documentación extendida: [`docs/`](docs)

---

## Cómo se aplica la mejora (flujo funcional)

1. La aplicación marca cada envío con `security_tag`.
2. `SecurityPolicyEngine` evalúa: perfil mínimo, perfil actual y capacidades remotas.
3. Si el mensaje requiere más seguridad, el `Link` puede iniciar upgrade PQC/híbrido.
4. Si el upgrade completa correctamente, se actualiza `key_version`.
5. Si no cumple política (por ejemplo `MAX_SECURITY` sin perfil suficiente), se bloquea con motivo.

Flujos y diagramas completos: [Arquitectura y cambios de seguridad adaptativa](docs/extended_security_adaptive_reticulum.md).

---

## Documentación técnica (meta-links internos)

- [Arquitectura y cambios de seguridad adaptativa](docs/extended_security_adaptive_reticulum.md)
- [Laboratorio local y pruebas extendidas](docs/local_lab_and_testing_extended.md)
- [Perfiles criptográficos](docs/crypto_profiles.md)
- [Security tags y Policy Engine](docs/security_tags_policy.md)
- [Flujo de upgrade PQC en Link](docs/link_pqc_upgrade.md)
- [Limitaciones conocidas](docs/limitations.md)
- [Roadmap técnico](docs/roadmap.md)
- [Índice documental](docs/architecture_index.md)

---

## Ejecución de laboratorio y pruebas

```bash
python lab_local/run_lab.py
python lab_local/run_lab.py --force-max-security
python lab_local/run_lab.py --force-max-security --network-profile lora_failure
python lab_local/run_lab.py --force-max-security --network-profile lora_extreme
python -m pytest -q tests/
```

Resultados y reportes:
- [`lab_local/results/latest_report.md`](lab_local/results/latest_report.md)
- [`lab_local/results/latest_report.json`](lab_local/results/latest_report.json)
- Logs por ejecución: [`lab_local/results/logs/`](lab_local/results/logs)

---

## Explicación criptográfica (más detallada, nivel práctico)

### Base clásica
- **Identidad/Firma**: Ed25519.
- **Intercambio clásico**: X25519 (ECDH).
- **Derivación**: HKDF (KDF basada en HMAC).
- **Cifrado de payload**: AES-256-CBC + HMAC-SHA256.

### Capa adaptativa añadida
- La política no trata todos los mensajes igual: usa `security_tag`.
- Para mensajes críticos (`MAX_SECURITY`), se exige perfil alto y se evita downgrade.
- Si el `Link` no cumple el perfil, se intenta upgrade híbrido/PQC.
- El cambio de clave se controla con `key_version` para evitar usar claves antiguas en tráfico crítico.

### Importante sobre PQC
Cuando ML-KEM/ML-DSA no están integrados de forma real y auditada, el resultado es:
- **SIMULATED** a nivel funcional,
- **NOT CONCLUSIVE** a nivel criptográfico.

Esto significa que el flujo de control puede estar validado, pero no constituye evidencia final de resistencia post-cuántica.

---

## Limitaciones clave

- Simulación LoRa local != comportamiento RF real.
- Falta validación completa con `tc/netem` kernel-level en todos los entornos.
- Falta integración real y auditoría externa de PQC.

Detalle: [Limitaciones conocidas](docs/limitations.md).

---

## Cómo continuar el desarrollo

Seguir fases en: [Roadmap técnico](docs/roadmap.md).

Resumen:
1. endurecer pruebas de fallo seguro,
2. integrar ML-KEM real,
3. validar ML-DSA si aplica,
4. ejecutar campañas con LoRa real,
5. auditoría criptográfica externa,
6. hardening operativo para red privada.


## Console Security Panel / TUI

- Ejecutar: `python -m rns_tui.app` o `./rns-security-panel`
- Documentación: [Panel TUI](docs/tui_panel.md)
- Configuración: `lab_local/panel_config.json`


- Self-test panel: `python -m rns_tui.app --self-test`
- Lab v2: `python lab_local/run_lab_v2.py --suite all --force-max-security --network-profile lora_failure`


## PQC real (backend)
- El backend principal es OpenSSL CLI en `RNS/pqc_backend.py`.
- Perfiles reales de sesión: `pqc512` (ML-KEM-512) y `pqc768` (ML-KEM-768).
- Si el backend no está disponible, los perfiles PQC fallan con error explícito: `ML-KEM backend not available`.
- `MAX_SECURITY` debe fallar cerrado si la política requiere PQC y no hay backend.

Nuevos docs:
- [PQC Reticulum LoRa (ES)](docs/pqc_reticulum_lora_es.md)
- [Labs Reticulum PQC (ES)](docs/labs_reticulum_pqc_es.md)
- [Glosario PQC Reticulum (ES)](docs/glosario_pqc_reticulum_es.md)


## Resultados medidos (resumen)

Sesión (ejecución real de referencia):
- standard: 61.532 s
- pqc512: 118.055 s (+56.523 s vs standard)
- pqc768: 122.056 s (+60.524 s vs standard)

Payloads:
- El tamaño cifrado y coste por mensaje son prácticamente iguales entre modos tras establecer sesión.
- La diferencia de coste está en el establecimiento inicial, no en cada payload.

Importante:
- Una anomalía observada mostró pública ML-KEM-512 más lenta que ML-KEM-768 en una corrida concreta por variabilidad LoRa/ACK/STATUS.
- No debe interpretarse como propiedad intrínseca del algoritmo.

Documentación completa de resultados:
- [Resultados LoRa PQC Reticulum (ES)](docs/resultados_lora_pqc_reticulum_es.md)
- [Decisión de funcionamiento](docs/decision_funcionamiento_reticulum_pqc_lora_es.md)
- [Laboratorios en español](docs/laboratorios_reticulum_pqc_lora_es.md)
- [Arquitectura de seguridad PQC](docs/arquitectura_seguridad_reticulum_pqc_es.md)
