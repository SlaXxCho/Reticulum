from pathlib import Path


def list_runs(base=Path('lab_local/results/logs')):
    if not base.exists():
        return []
    return sorted([p.name for p in base.iterdir() if p.is_dir()])


def list_logs(run):
    p = Path('lab_local/results/logs') / run
    if not p.exists():
        return []
    return sorted([x.name for x in p.iterdir() if x.is_file()])
