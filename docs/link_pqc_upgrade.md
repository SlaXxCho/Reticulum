# Link PQC Upgrade (Documented Behavior)

1. Establish classical link.
2. Exchange capabilities.
3. Evaluate message policy.
4. If required, start PQC upgrade flow.
5. Exchange PQC material (real or simulated, depending on build).
6. Derive next key using `HKDF(old_key || pqc_secret)`.
7. Confirm key switch.
8. Increase `key_version` and allow strict traffic (`MAX_SECURITY`).

## Risks and failure modes
- Downgrade attacks (capability stripping, forced classic).
- Replay of old control messages.
- Key desynchronization during cutover.
- Fragment loss/corruption in low-MTU links.
- DoS via repeated failed negotiations.
- False confidence when PQC is simulated.

## Safety expectation
If upgrade does not complete/verify, strict messages must block and key version must not advance.
