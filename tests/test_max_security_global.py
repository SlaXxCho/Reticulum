from RNS.crypto_profiles import CryptoProfileManager
from RNS.security_policy import SecurityPolicyEngine

def test_max_security_blocks_classic():
    d=SecurityPolicyEngine(CryptoProfileManager()).evaluate("MAX_SECURITY",{"classic":{}},"classic")
    assert d["block"] is True
