import hashlib
import RNS


def derive(shared, link_id, session_id, profile, epoch):
    salt = hashlib.sha256((link_id+session_id+profile+str(epoch)).encode()).digest()
    info = ("RNS-PQC-SESSION-v1|"+profile).encode()
    return RNS.Cryptography.hkdf(length=32, derive_from=shared, salt=salt, context=info)


def test_deterministic_key_same_input():
    a = derive(b'x'*32,'l','s','pqc512',1)
    b = derive(b'x'*32,'l','s','pqc512',1)
    assert a == b


def test_diff_session_id_changes_key():
    a = derive(b'x'*32,'l','s1','pqc512',1)
    b = derive(b'x'*32,'l','s2','pqc512',1)
    assert a != b


def test_diff_profile_changes_key():
    a = derive(b'x'*32,'l','s','pqc512',1)
    b = derive(b'x'*32,'l','s','pqc768',1)
    assert a != b
