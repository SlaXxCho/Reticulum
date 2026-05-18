import os
import time
import threading
import hashlib

import RNS
from RNS.vendor import umsgpack
from RNS.pqc_backend import encapsulate, PQCBackendUnavailable


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

    def build_kem_exchange(self, profile_name, receiver_public_key: bytes | None = None):
        if profile_name not in ("pqc512", "pqc768"):
            fake_ciphertext = os.urandom(64)
            payload = umsgpack.packb({"t": "PQC_KEM", "profile": profile_name, "ct": fake_ciphertext, "n": self._nonce(), "ts": time.time(), "simulated": True})
            return self.CONTROL_PREFIX + payload

        if receiver_public_key is None:
            raise PQCBackendUnavailable("ML-KEM backend not available")

        alg = "ML-KEM-512" if profile_name == "pqc512" else "ML-KEM-768"
        ct, ss = encapsulate(alg, receiver_public_key)
        payload = umsgpack.packb({
            "t": "PQC_KEM", "profile": profile_name, "kex_alg": alg,
            "ct": ct,
            "ct_sha256": hashlib.sha256(ct).hexdigest()[:16],
            "n": self._nonce(), "ts": time.time(), "simulated": False
        })
        return self.CONTROL_PREFIX + payload, ss

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
