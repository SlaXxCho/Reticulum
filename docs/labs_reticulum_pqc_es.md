# Laboratorios Reticulum PQC (ES)

## Verificar backend
```bash
python -m pytest -q tests/test_pqc_backend.py
```

## Menú terminal
```bash
python -m rns_tui.lora_pqc_menu --self-test
```

## Benchmark productivo simulado
```bash
python lab_local/reticulum_pqc_prod/run_prod_benchmark.py --self-test
python lab_local/reticulum_pqc_prod/run_prod_benchmark.py --role receiver --port /dev/ttyACM1 --profiles classic,pqc512,pqc768 --run-id demo_001
python lab_local/reticulum_pqc_prod/run_prod_benchmark.py --role transmitter --port /dev/ttyACM0 --profiles classic,pqc512,pqc768 --run-id demo_001
```

## Resultados
Se generan:
- `report.md`
- `summary_metrics.json`
- `events.jsonl`
- `transfers.csv`
- `security_tests.csv`
- `.tar.gz` exportable

Si el backend no soporta ML-KEM, perfiles PQC quedan `backend_unavailable`.
