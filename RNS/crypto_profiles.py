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
    def __init__(self, name, signing, kex, payload_cipher="AES-256-GCM", pqc=False, low_bandwidth=False, recommended=False):
        self.name = name
        self.signing = signing
        self.kex = kex
        self.payload_cipher = payload_cipher
        self.pqc = pqc
        self.low_bandwidth = low_bandwidth
        self.recommended = recommended

    @property
    def requires_pqc(self):
        return self.pqc


class CryptoProfileManager:
    PROFILES = {
        "classic": CryptoProfile("classic", signing="Ed25519", kex="X25519", pqc=False),
        "pqc512": CryptoProfile("pqc512", signing="Ed25519", kex="ML-KEM-512", pqc=True, low_bandwidth=True),
        "pqc768": CryptoProfile("pqc768", signing="Ed25519", kex="ML-KEM-768", pqc=True, recommended=True),
        # compat legacy aliases
        "hybrid_light": CryptoProfile("hybrid_light", signing="Ed25519", kex="X25519+ML-KEM-512", pqc=True, low_bandwidth=True),
        "hybrid_strong": CryptoProfile("hybrid_strong", signing="Ed25519+ML-DSA", kex="X25519+ML-KEM-768", pqc=True, recommended=True),
        "pqc_experimental": CryptoProfile("pqc_experimental", signing="ML-DSA", kex="ML-KEM", pqc=True),
    }

    ORDER = ["classic", "pqc512", "pqc768", "hybrid_light", "hybrid_strong", "pqc_experimental"]

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
        return self.ORDER.index(profile_name)

    def can_downgrade_to(self, profile_name):
        return self.rank(profile_name) >= self.rank(self.minimum_profile)

    def choose_best_common(self, remote_capabilities, medium=Medium.UNKNOWN):
        available = [p for p in self.PROFILES if p in remote_capabilities and self.can_downgrade_to(p)]
        if not available:
            return None
        if medium == Medium.LORA:
            preferred = ["pqc512", "classic", "pqc768", "hybrid_light", "hybrid_strong", "pqc_experimental"]
        else:
            preferred = ["pqc768", "pqc512", "hybrid_strong", "hybrid_light", "classic", "pqc_experimental"]
        for p in preferred:
            if p in available:
                return self.get_profile(p)
        return self.get_profile(max(available, key=self.rank))
