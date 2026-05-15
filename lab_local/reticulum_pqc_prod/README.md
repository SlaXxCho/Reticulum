# Reticulum PQC Prod Lab (experimental)

Ejecución:
- `python lab_local/reticulum_pqc_prod/run_prod_benchmark.py --self-test`
- `python lab_local/reticulum_pqc_prod/run_prod_benchmark.py --role receiver --port /dev/ttyACM1 --profiles classic,pqc512,pqc768 --run-id demo_001`
- `python lab_local/reticulum_pqc_prod/run_prod_benchmark.py --role transmitter --port /dev/ttyACM0 --profiles classic,pqc512,pqc768 --run-id demo_001`

Si ML-KEM no está disponible, pqc512/pqc768 reportan `backend_unavailable` (fallo explícito).
