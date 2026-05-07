from rns_tui.report_loader import redact

def test_secret_redaction_patterns():
    t='private_key shared_secret session_key hkdf symmetric_key seed raw_key plaintext_key'
    r=redact(t)
    assert '<REDACTED>' in r
    assert 'shared_secret' not in r
