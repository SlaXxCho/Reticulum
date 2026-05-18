from pathlib import Path
from rns_tui.config import load_config, save_config


def test_config_save_load(tmp_path: Path):
    p = tmp_path / 'panel_config.json'
    save_config({'min_profile': 'hybrid_light'}, p)
    cfg = load_config(p)
    assert cfg['min_profile'] == 'hybrid_light'
    assert 'default_security_tag' in cfg
