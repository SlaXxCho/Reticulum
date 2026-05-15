from RNS.crypto_profiles import CryptoProfileManager
from RNS.security_policy import SecurityPolicyEngine

def test_active_downgrade_blocked_for_max_security():
    d=SecurityPolicyEngine(CryptoProfileManager(minimum_profile='hybrid_light')).evaluate('MAX_SECURITY',{'classic':{}},'classic')
    assert d['block'] is True
