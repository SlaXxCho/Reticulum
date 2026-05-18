from RNS.pqc_upgrade import PQCUpgradeManager
class D: 
    def get_salt(self): return b'salt'

def test_corrupted_control_rejected():
    m=PQCUpgradeManager(D())
    try:
        m.parse_control(PQCUpgradeManager.CONTROL_PREFIX+b'\xff\xff')
        assert False
    except Exception:
        assert True
