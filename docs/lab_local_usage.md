# Local Lab Usage

## Run
```bash
python lab_local/run_lab.py
python lab_local/run_lab.py --force-max-security
python lab_local/run_lab.py --force-max-security --network-profile lora_failure
python lab_local/run_lab.py --force-max-security --network-profile lora_extreme
```

## How it works
- Starts local subprocess nodes (`node_a`, `node_b`, `node_c`).
- Applies network profile parameters from `lab_local/network_profiles.py`.
- Uses `tc/netem` if available; otherwise Python fallback simulation.
- Writes:
  - `lab_local/results/latest_report.md`
  - `lab_local/results/latest_report.json`
  - `lab_local/results/logs/<timestamp>/...`

## Network profiles
`normal`, `wifi_like`, `ethernet_like`, `lora_basic`, `lora_degraded`, `lora_failure`, `lora_extreme`.

## Note
Local simulation is useful for functional validation, but **not equivalent** to RF LoRa behavior.
