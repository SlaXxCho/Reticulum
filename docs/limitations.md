# Limitaciones y riesgos

- PQC simulado/mock **no equivale** a seguridad post-cuántica real. (**SIMULATED / NOT CONCLUSIVE**)
- LoRa simulado **no equivale** a LoRa físico en RF. (**SIMULATED / NOT CONCLUSIVE**)
- Falta integrar y validar ML-KEM real. (**TODO**)
- Falta integrar y validar ML-DSA real (si se mantiene identidad híbrida). (**TODO**)
- Falta validar con `tc/netem` kernel-level real. (**TODO**)
- Falta campaña con hardware LoRa real. (**TODO**)
- Falta medir consumo energético, duty cycle y colisiones RF. (**TODO**)
- Falta análisis DoS específico del flujo de upgrade. (**TODO**)
- Falta auditoría criptográfica externa independiente. (**TODO**)

## Etiquetas de estado
- **VALIDATED**: evidencia funcional en pruebas.
- **SIMULATED**: comportamiento emulado por harness.
- **NOT CONCLUSIVE**: no permite afirmación criptográfica final.
- **TODO**: pendiente técnico.
