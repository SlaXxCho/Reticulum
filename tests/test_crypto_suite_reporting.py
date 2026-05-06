from lab_local.run_lab import crypto_block

def test_crypto_block_no_secrets_and_has_sizes():
    c=crypto_block('hybrid_light',2,True)
    assert c['key_exchange_pqc']['ciphertext_size']>0
    rendered=str(c)
    assert 'private_key' not in rendered
    assert 'session_key' not in rendered
    assert 'shared_secret =' not in rendered
