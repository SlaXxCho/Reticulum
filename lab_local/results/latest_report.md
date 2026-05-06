# Local Lab Report
- suite: maximum_security_failure_suite
- force_max_security: True
- network_profile: lora_failure
- tc/netem available: False
- fallback: True

## Scenario | Network | Tag | Requested | Negotiated | PQC | Key Before | Key After | Failure | Result | Notes
---|---|---|---|---|---|---|---|---|---|---
classic_standard | lora_failure | MAX_SECURITY | hybrid_light | classic | failed | 1 | 1 | - | FAIL | -
hybrid_light_upgrade | lora_failure | MAX_SECURITY | hybrid_light | hybrid_light | ok | 1 | 2 | - | OK | -
max_security_block_without_pqc | lora_failure | MAX_SECURITY | hybrid_light | n/a | failed | 1 | 1 | max_security_block | OK | required profile not available
replay_policy_update_rejected | lora_failure | MAX_SECURITY | hybrid_light | n/a | failed | 1 | 1 | replay | OK | replay rejected
key_desync_safe_failure | lora_failure | MAX_SECURITY | hybrid_light | n/a | failed | 1 | 1 | key_desync | OK | unexpected key_version
false_positive_guard_forced_pqc_failure | lora_failure | MAX_SECURITY | hybrid_light | hybrid_light | failed | 1 | 1 | pqc_forced_fail | OK | pqc upgrade failed

## Limitaciones de validez de las pruebas
- PQC: SIMULATED / NOT CONCLUSIVE
- LoRa: fallback Python si tc no está disponible
- Hardware LoRa real pendiente
## Documentation Clarification

- This report demonstrates **functional behavior in a local harness**.
- PQC-related outcomes in this run are **SIMULATED / NOT CONCLUSIVE** unless backed by real PQC cryptographic implementations and independent verification.
- Network impairment in this environment used fallback simulation when `tc/netem` was unavailable.
