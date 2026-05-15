import pytest
from RNS.pqc_upgrade import PQCUpgradeManager

class L: 
    def get_salt(self): return b'salt'


def test_replay_blocked():
    m=PQCUpgradeManager(L())
    raw=m.build_policy_update('pqc512')
    m.parse_control(raw)
    with pytest.raises(ValueError):
        m.parse_control(raw)
