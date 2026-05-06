import json
from pathlib import Path

REPORT_JSON = Path('lab_local/results/latest_report.json')

SENSITIVE = ['private_key', 'shared_secret', 'session_key']


def redact(text: str):
    out = text
    for k in SENSITIVE:
        out = out.replace(k, '[REDACTED_KEY]')
    return out


def load_latest_report(path=REPORT_JSON):
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return json.loads(redact(json.dumps(data)))
