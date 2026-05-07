# Console Security Panel / TUI

## Ejecución
```bash
python -m rns_tui.app
./rns-security-panel
python -m rns_tui.app --debug
```

## Funciones
- Ver política local (`lab_local/panel_config.json`).
- Ver perfiles criptográficos y estado REAL/MOCK/SIMULATED.
- Ejecutar laboratorio local (`lab_local/run_lab.py`).
- Ejecutar grupos de tests (basic/security/extended/negative).
- Cargar `latest_report.json` con redacción de términos sensibles.
- Ver entorno (Python/OS/git).

## Seguridad del panel
- No muestra secretos ni claves privadas.
- Redacta tokens de texto sensibles (`private_key`, `shared_secret`, `session_key`).

## Limitaciones
- Implementación actual: menú CLI fallback (sin Textual), para máxima compatibilidad.
- Visualización en tiempo real y filtros avanzados de logs: TODO.

## Configuración
Se guarda en `lab_local/panel_config.json` con campos:
- `min_profile`, `max_profile`, `default_profile`
- `allow_downgrade`, `require_pqc`, `force_max_security`
- `default_security_tag`, `network_profile`


## Self-test
```bash
python -m rns_tui.app --self-test
```
Genera `lab_local/results/tui_self_test.md` y `.json`.
