import pytest
from RNS.pqc_backend import supports_alg, backend_info, generate_keypair, encapsulate, decapsulate, PQCBackendUnavailable


def test_backend_info():
    info = backend_info()
    assert 'backend' in info and 'supports' in info


def test_mlkem_512_roundtrip_or_skip():
    if not supports_alg('ML-KEM-512'):
        pytest.skip('ML-KEM backend not available')
    kp = generate_keypair('ML-KEM-512')
    ct, ss1 = encapsulate('ML-KEM-512', kp.public_key)
    ss2 = decapsulate('ML-KEM-512', kp.private_key, ct)
    assert ss1 == ss2


def test_mlkem_768_roundtrip_or_skip():
    if not supports_alg('ML-KEM-768'):
        pytest.skip('ML-KEM backend not available')
    kp = generate_keypair('ML-KEM-768')
    ct, ss1 = encapsulate('ML-KEM-768', kp.public_key)
    ss2 = decapsulate('ML-KEM-768', kp.private_key, ct)
    assert ss1 == ss2
