import json
from pathlib import Path

CONFIG_PATH = Path('lab_local/panel_config.json')
DEFAULT_CONFIG = {
    'min_profile': 'classic', 'max_profile': 'pqc_experimental', 'default_profile': 'classic',
    'allow_downgrade': True, 'require_pqc': False, 'force_max_security': False,
    'default_security_tag': 'STANDARD', 'network_profile': 'normal'
}


def load_config(path=CONFIG_PATH):
    if path.exists():
        return {**DEFAULT_CONFIG, **json.loads(path.read_text())}
    return dict(DEFAULT_CONFIG)


def save_config(cfg, path=CONFIG_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cfg, indent=2))
