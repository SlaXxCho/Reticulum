# PQC en Reticulum sobre LoRa (ES)

Este documento explica el enfoque real de sesión PQC:
- ML-KEM se usa para **establecer secreto compartido de sesión** (KEX/KEM),
- el contenido se cifra con AES-256-GCM,
- luego el transporte/fragmentación LoRa mueve bytes ya cifrados.

## classic vs pqc512 vs pqc768
- classic: X25519 + HKDF + cifrado simétrico.
- pqc512: ML-KEM-512 para sesión (útil bajo ancho de banda).
- pqc768: ML-KEM-768 (perfil recomendado seguro).

## Por qué no PQC por chunk
El coste fuerte de PQC está en el establecimiento de sesión. Repetir KEM por fragmento empeora latencia/throughput sin beneficio práctico.

## Conceptos
- KEX: intercambio de claves.
- KEM: encapsulación para obtener secreto compartido.
- HKDF: derivación de `session_key`.
- key_epoch: versión de clave de sesión.
- anti-replay: bloqueo de mensajes repetidos.
- TOFU/pinning: confianza de primera vez y validación de huella.

## Estado
- Si backend ML-KEM no existe: error explícito `ML-KEM backend not available`.
- No se declara seguridad PQC real si el backend no está disponible.
