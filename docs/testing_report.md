# Testing Report (Current Lab State)

## Scope
- Unit tests
- Negative/failure-mode tests
- Local integration/lab scenarios
- Anti-downgrade and replay checks
- Key cutover/desync checks
- LoRa-like fragmentation/loss simulation

## Known reported results
- Lab scenarios: **16/16 OK** (baseline run set in prior validated report).
- Extended pytest set: **40 passed** (prior validated report).
- `tc/netem` unavailable in current host runs -> fallback simulation used.
- PQC path in lab context: **SIMULATED / NOT CONCLUSIVE**.

## Reproduction commands
```bash
pytest -q tests/test_crypto_profiles.py tests/test_security_policy.py tests/test_pqc_upgrade.py tests/test_link_security_tags.py tests/test_anti_downgrade.py tests/test_replay_protection.py tests/test_key_desync.py tests/test_lora_fragmentation.py

python lab_local/run_lab.py

python -m pytest -q tests/test_crypto_profiles.py tests/test_security_policy.py tests/test_pqc_upgrade.py tests/test_link_security_tags.py tests/test_anti_downgrade.py tests/test_replay_protection.py tests/test_key_desync.py tests/test_lora_fragmentation.py tests/test_policy_matrix.py tests/test_key_versioning_extended.py tests/test_security_policy_update.py tests/test_lora_stress.py
```

## Interpretation guidance
- **VALIDATED**: functional behavior observed in tests.
- **SIMULATED**: behavior emulated by harness/mocks.
- **NOT CONCLUSIVE**: cannot claim cryptographic proof-level assurance from this dataset.


## Panel/TUI y Lab v2
- Self-test TUI: `python -m rns_tui.app --self-test`
- Lab v2: suites `basic`, `security`, `failure`, `all`
- Estado PQC y red degradada: **SIMULATED / NOT CONCLUSIVE**.
