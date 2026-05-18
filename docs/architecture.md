# Adaptive Security Architecture (Lab Extension)

> Scope: documentation of the local/lab extension added in this fork. Not production guidance.

## High-level flow

```text
Application
  ↓ (security_tag)
SecurityPolicyEngine
  ↓ (allow/block/upgrade)
Link
  ↓ (control messages)
PQCUpgradeManager
  ↓ (HKDF + key_version)
Packet / Transport
```

## Policy layers
- **Node policy**: minimum profile boundary.
- **Link policy**: negotiated profile/capabilities for the peer.
- **Message policy**: `security_tag` on each send decision.

## Security controls
- Anti-downgrade checks against required profile and peer capabilities.
- Replay checks for security-control messages (nonce-based).
- Key transition tracking through `key_version` and switch confirmation semantics.

## Link state model (documented target)
`INIT -> ESTABLISHED -> PQC_NEGOTIATION -> KEY_SWITCH -> SECURE`

## Terminology
- **PQC**: Post-Quantum Cryptography.
- **KEM**: Key Encapsulation Mechanism.
- **HKDF**: HMAC-based Key Derivation Function.
- **ECDH**: Elliptic Curve Diffie-Hellman.
- **MTU**: Maximum Transmission Unit.
