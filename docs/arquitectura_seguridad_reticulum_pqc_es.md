# Arquitectura de seguridad Reticulum PQC (ES)

## Módulos
- `RNS/pqc_backend.py`: backend PQC real (OpenSSL CLI), detección y encapsulación/decapsulación.
- `RNS/crypto_profiles.py`: perfiles `classic`, `pqc512`, `pqc768` (+legacy compat).
- `RNS/security_policy.py`: reglas de `security_tag` y fail-closed para `MAX_SECURITY`.
- `RNS/pqc_upgrade.py`: control messages, anti-replay nonce, KEM exchange.

## Flujo
1. Session setup (`classic` X25519 o `pqc512/pqc768` ML-KEM).
2. HKDF-SHA256 -> `session_key`.
3. AES-256-GCM en payload completo.
4. Fragmentación/transporte LoRa.

## Controles
- Anti-replay (`message_id`/nonce control).
- Anti-downgrade por policy.
- TOFU/pinning/fingerprint.
- Fail-closed para `MAX_SECURITY` sin backend PQC.

## Trazabilidad
- JSONL (`events.jsonl`) con tags de auditoría.
- CSV por sesión, payload y seguridad.
- Resúmenes JSON y `report.md` en español.

## No exportar secretos
- private keys
- shared secrets
- session keys
- material HKDF interno
