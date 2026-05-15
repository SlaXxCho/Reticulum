# Lab V2 Report
- suite: failure
- force_max_security: False
- network_profile: normal

Scenario | Suite | Result | Negotiated | Notes
---|---|---|---|---
forced_pqc_failure | failure | OK | hybrid_light | SIMULATED / NOT CONCLUSIVE
corrupted_kem_ciphertext | failure | OK | hybrid_light | SIMULATED / NOT CONCLUSIVE
lost_lora_fragment | failure | OK | hybrid_light | SIMULATED / NOT CONCLUSIVE
duplicated_lora_fragment | failure | OK | hybrid_light | SIMULATED / NOT CONCLUSIVE
out_of_order_fragments | failure | OK | hybrid_light | SIMULATED / NOT CONCLUSIVE
key_switch_interrupted | failure | OK | hybrid_light | SIMULATED / NOT CONCLUSIVE
max_security_lora_failure | failure | OK | hybrid_light | SIMULATED / NOT CONCLUSIVE
max_security_lora_extreme | failure | OK | hybrid_light | SIMULATED / NOT CONCLUSIVE

## Limitaciones
- SIMULATED / NOT CONCLUSIVE