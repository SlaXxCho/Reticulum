# Cryptographic Profiles

## Profiles
- `classic`: Ed25519 + X25519.
- `hybrid_light`: Ed25519 + X25519 + ML-KEM-512.
- `hybrid_strong`: Ed25519 + ML-DSA + X25519 + ML-KEM-768.
- `pqc_experimental`: ML-DSA + ML-KEM.

## Comparison
| Profile | Identity | Key exchange | KDF | Symmetric/Auth | Recommended use | Cost | Medium fit | Status |
|---|---|---|---|---|---|---|---|---|
| classic | Ed25519 | X25519 | HKDF | AES-256-CBC + HMAC-SHA256 | baseline compatibility | low | LoRa/WiFi/Ethernet | VALIDATED (functional) |
| hybrid_light | Ed25519 | X25519 + ML-KEM-512 | HKDF | AES-256-CBC + HMAC-SHA256 | constrained links requiring stronger policy | medium | LoRa (preferred hybrid), WiFi | SIMULATED / NOT CONCLUSIVE for PQC |
| hybrid_strong | Ed25519 + ML-DSA | X25519 + ML-KEM-768 | HKDF | AES-256-CBC + HMAC-SHA256 | stronger private-network posture | high | WiFi/Ethernet | SIMULATED / NOT CONCLUSIVE for PQC |
| pqc_experimental | ML-DSA | ML-KEM | HKDF | AES-256-CBC + HMAC-SHA256 | research only | very high/unknown | WiFi/Ethernet | SIMULATED / NOT CONCLUSIVE |

> Important: PQC material in this lab path is currently simulated/mock-oriented unless explicitly integrated with real PQC libraries.
