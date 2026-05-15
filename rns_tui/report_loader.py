import json
from pathlib import Path

REPORT_JSON = Path('lab_local/results/latest_report.json')
SENSITIVE = ['private_key', 'shared_secret', 'session_key', 'hkdf', 'symmetric_key', 'seed', 'raw_key', 'plaintext_key']


def redact(text: str):
    out = text
    for k in SENSITIVE:
        out = out.replace(k, '<REDACTED>')
    return out


def load_latest_report(path=REPORT_JSON):
    if not path.exists():
        return {'message': 'No report available. Run lab first.'}
    raw = path.read_text().strip()
    if not raw:
        return {'message': 'No report available. Run lab first.'}
    try:
        data = json.loads(raw)
    except Exception:
        return {'error': 'Invalid report JSON'}
    return json.loads(redact(json.dumps(data)))
