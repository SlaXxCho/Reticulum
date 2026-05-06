# Limitations and Validation Boundaries

- **PQC integration status**: may be simulated/mock in lab flows.
  - Label: **SIMULATED / NOT CONCLUSIVE**
- **Real PQC assurances**: not established unless ML-KEM/ML-DSA real implementations are integrated and audited.
  - Label: **NOT CONCLUSIVE**
- **Network emulation**: current environment reported no `tc/netem`; fallback simulation used.
  - Label: **SIMULATED**
- **LoRa RF validation**: no hardware RF tests in this environment.
  - Label: **NOT CONCLUSIVE**
- **Duty cycle, RF collisions, energy profile**: not measured.
  - Label: **TODO**
- **Fragmentation validation**: logical/software-level behavior validated; physical LoRa stack behavior pending.
  - Label: **VALIDATED (logic) / NOT CONCLUSIVE (RF)**
- **Production readiness**: not production-hardening complete.
  - Label: **TODO**
