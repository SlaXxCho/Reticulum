from pathlib import Path
from rns_tui.report_loader import load_latest_report, redact


def test_redact_sensitive_text():
    t = 'private_key aaa shared_secret bbb session_key ccc'
    r = redact(t)
    assert '[REDACTED_KEY]' in r


def test_load_report(tmp_path: Path):
    p = tmp_path / 'latest_report.json'
    p.write_text('{"ok":true}')
    d = load_latest_report(p)
    assert d['ok'] is True
