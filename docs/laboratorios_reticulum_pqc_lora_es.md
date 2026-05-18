# Laboratorios Reticulum PQC LoRa (ES)

## Preparación
1. Verificar OpenSSL y soporte ML-KEM:
```bash
python -m pytest -q tests/test_pqc_backend.py
```
2. Si backend no soporta ML-KEM, perfiles PQC deben fallar explícitamente (`backend_unavailable`).

## Ejecución
### Receiver
```bash
python lab_local/reticulum_pqc_prod/run_prod_benchmark.py --role receiver --port /dev/ttyACM1 --profiles classic,pqc512,pqc768 --run-id reticulum_pqc_prod_003 --repeat 3
```
### Transmitter
```bash
python lab_local/reticulum_pqc_prod/run_prod_benchmark.py --role transmitter --port /dev/ttyACM0 --profiles classic,pqc512,pqc768 --run-id reticulum_pqc_prod_003 --repeat 3
```

## Lectura de resultados
- `report.md`: narrativa y tablas.
- `summary_metrics.json`: configuración y recomendación.
- `summary_statistics.json`: media/mediana/min/max/p95 (si aplica).
- `events.jsonl`: trazabilidad de eventos.
- `sessions.csv`, `payloads.csv`, `transfers.csv`, `security_tests.csv`, `anomalies.csv`.

## Interpretación de anomalías
- `rc=-15` en procesos controlados puede ser terminación gestionada.
- `timeout=False` no implica éxito criptográfico; verificar `result` y `backend_unavailable`.
- `found=...` depende del flujo de parsing/estado.

## Repeticiones
Usar `--repeat N`; evitar conclusiones con una sola muestra. Priorizar mediana y p95.
