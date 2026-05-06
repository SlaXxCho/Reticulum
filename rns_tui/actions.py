from .config import load_config, save_config
from .runner import build_lab_command, run_command, predefined_test_commands
from .report_loader import load_latest_report


def run_lab(cfg):
    cmd = build_lab_command(cfg.get('force_max_security', False), cfg.get('network_profile'))
    return cmd, run_command(cmd)


def run_tests(group):
    cmd = predefined_test_commands()[group]
    return cmd, run_command(cmd)


def latest_report():
    return load_latest_report()


def update_config(changes):
    cfg = load_config()
    cfg.update(changes)
    save_config(cfg)
    return cfg
