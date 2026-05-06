# Laboratorio local y pruebas extendidas

## Estructura
- `lab_local/run_lab.py`: orquestador principal.
- `lab_local/node_a.py`, `node_b.py`, `node_c.py`: nodos simulados por subprocess.
- `lab_local/netem.py`: wrapper/fallback de emulación de red.
- `lab_local/network_profiles.py`: perfiles de red simulados.
- `lab_local/results/`: reportes y logs por ejecución.

## Comandos
```bash
python lab_local/run_lab.py
python lab_local/run_lab.py --force-max-security
python lab_local/run_lab.py --force-max-security --network-profile lora_failure
python lab_local/run_lab.py --force-max-security --network-profile lora_extreme
python -m pytest -q tests/
```

## Qué valida
- policy decisions por tag,
- downgrade/replay,
- key cutover y desync,
- fragmentación/loss simulados,
- fail-safe en escenarios degradados,
- guardas de falsos positivos.

## PASS / FAIL / SIMULATED
- **PASS**: comportamiento esperado observado en entorno de prueba.
- **FAIL**: desviación detectada (debe analizarse, no ocultarse).
- **SIMULATED / NOT CONCLUSIVE**: no afirmar conclusiones criptográficas reales.

## Resultados actuales conocidos (histórico reportado)
- 16/16 escenarios OK (corridas base previas documentadas).
- 40 tests passed (suite extendida reportada).
- False-positive guard incluido.
- Replay rechazado.
- Downgrade bloqueado.
- Key desync falla seguro.
- Fragmentación LoRa simulada validada lógicamente.
- `tc/netem` no disponible en entorno observado: fallback local usado.
- PQC real no concluyente si ML-KEM/ML-DSA están mock/simulados.

## Tabla resumen
| Prueba | Objetivo | Resultado | Qué demuestra | Limitación |
|---|---|---|---|---|
| classic_standard | baseline | OK/según suite | interoperabilidad básica | no mide PQC real |
| hybrid_light_upgrade | upgrade | OK | transición de perfil | PQC simulado |
| max_security_block_without_pqc | anti-downgrade | OK | bloqueo seguro | entorno simulado |
| anti_downgrade_block | ataque downgrade | OK | enforcement policy | no MITM real |
| replay_policy_update_rejected | replay | OK | rechazo nonce repetido | no red hostil real |
| key_desync_safe_failure | cutover | OK | fail-safe de versión | no throughput real |
| lora_fragmentation_hybrid_light | bajo MTU | OK | manejo lógico de fragmentación | no RF real |
| false_positive_guard_forced_pqc_failure | control calidad | OK | evita éxito falso | depende del harness |
