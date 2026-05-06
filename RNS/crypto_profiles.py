import enum


class SecurityTag(enum.Enum):
    MAX_SECURITY = "MAX_SECURITY"
    MUST_DELIVER = "MUST_DELIVER"
    PREFERRED_SECURE = "PREFERRED_SECURE"
    STANDARD = "STANDARD"


class Medium(enum.Enum):
    LORA = "LoRa"
    WIFI = "WiFi"
    ETHERNET = "Ethernet"
    UNKNOWN = "Unknown"


class CryptoProfile:
    def __init__(self, name, signing, kex, pqc_signing=None, pqc_kem=None):
        self.name = name
        self.signing = signing
        self.kex = kex
        self.pqc_signing = pqc_signing
        self.pqc_kem = pqc_kem

    @property
    def is_hybrid(self):
        return self.pqc_kem is not None or self.pqc_signing is not None

    @property
    def requires_pqc(self):
        return self.name in ("hybrid_light", "hybrid_strong", "pqc_experimental")


class CryptoProfileManager:
    PROFILES = {
        "classic": CryptoProfile("classic", signing="Ed25519", kex="X25519"),
        "hybrid_light": CryptoProfile("hybrid_light", signing="Ed25519", kex="X25519", pqc_kem="ML-KEM-512"),
        "hybrid_strong": CryptoProfile("hybrid_strong", signing="Ed25519", kex="X25519", pqc_signing="ML-DSA", pqc_kem="ML-KEM-768"),
        "pqc_experimental": CryptoProfile("pqc_experimental", signing="ML-DSA", kex="ML-KEM", pqc_signing="ML-DSA", pqc_kem="ML-KEM"),
    }

    def __init__(self, minimum_profile="classic", preferred_profile="classic"):
        self.minimum_profile = minimum_profile
        self.preferred_profile = preferred_profile

    def get_profile(self, profile_name):
        if profile_name not in self.PROFILES:
            raise ValueError(f"Unknown crypto profile: {profile_name}")
        return self.PROFILES[profile_name]

    def get_capabilities(self):
        return {name: self.PROFILES[name].__dict__.copy() for name in self.PROFILES}

    def rank(self, profile_name):
        order = ["classic", "hybrid_light", "hybrid_strong", "pqc_experimental"]
        return order.index(profile_name)

    def can_downgrade_to(self, profile_name):
        return self.rank(profile_name) >= self.rank(self.minimum_profile)

    def choose_best_common(self, remote_capabilities, medium=Medium.UNKNOWN):
        available = []
        for profile_name in self.PROFILES:
            if profile_name in remote_capabilities and self.can_downgrade_to(profile_name):
                available.append(profile_name)

        if not available:
            return None

        if medium == Medium.LORA:
            preferred = ["hybrid_light", "classic", "hybrid_strong", "pqc_experimental"]
        else:
            preferred = ["hybrid_strong", "hybrid_light", "pqc_experimental", "classic"]

        for p in preferred:
            if p in available:
                return self.get_profile(p)

        return self.get_profile(max(available, key=self.rank))
