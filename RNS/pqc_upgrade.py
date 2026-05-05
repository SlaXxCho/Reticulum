import os
import time
import threading

import RNS
from RNS.vendor import umsgpack


class PQCUpgradeManager:
    CONTROL_PREFIX = b"RNSSEC1"

    def __init__(self, link):
        self.link = link
        self.nonce_lock = threading.Lock()
        self.seen_nonces = set()

    def _nonce(self):
        return os.urandom(12)

    def build_capability_message(self, capabilities):
        payload = umsgpack.packb({"t": "CAPS", "caps": capabilities, "ts": time.time(), "n": self._nonce()})
        return self.CONTROL_PREFIX + payload

    def build_policy_update(self, requested_profile, duration=120):
        payload = umsgpack.packb({
            "t": "SECURITY_POLICY_UPDATE",
            "requested_profile": requested_profile,
            "duration": duration,
            "nonce": self._nonce(),
            "ts": time.time(),
        })
        return self.CONTROL_PREFIX + payload

    def build_kem_exchange(self, profile_name):
        fake_ciphertext = os.urandom(64)
        payload = umsgpack.packb({"t": "PQC_KEM", "profile": profile_name, "ct": fake_ciphertext, "n": self._nonce(), "ts": time.time()})
        return self.CONTROL_PREFIX + payload

    def parse_control(self, plaintext):
        if not plaintext.startswith(self.CONTROL_PREFIX):
            return None
        data = umsgpack.unpackb(plaintext[len(self.CONTROL_PREFIX):])
        n = data.get("n") or data.get("nonce")
        if n:
            with self.nonce_lock:
                if n in self.seen_nonces:
                    raise ValueError("Replay detected for security control message")
                self.seen_nonces.add(n)
                if len(self.seen_nonces) > 2048:
                    self.seen_nonces = set(list(self.seen_nonces)[-1024:])
        return data

    def derive_hybrid_material(self, old_derived_key, pqc_shared_secret):
        return RNS.Cryptography.hkdf(
            length=len(old_derived_key),
            derive_from=old_derived_key + pqc_shared_secret,
            salt=self.link.get_salt(),
            context=b"RNS-PQC-UPGRADE",
        )
