import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass


class PQCBackendUnavailable(RuntimeError):
    pass


@dataclass
class PQCKeyPair:
    algorithm: str
    public_key: bytes
    private_key: bytes


ALG_MAP = {"ML-KEM-512": "ML-KEM-512", "ML-KEM-768": "ML-KEM-768"}


def _openssl_version() -> str:
    if shutil.which("openssl") is None:
        return "openssl-not-found"
    p = subprocess.run(["openssl", "version"], capture_output=True, text=True)
    return (p.stdout or p.stderr).strip()


def backend_info() -> dict:
    return {
        "backend": "openssl-cli",
        "openssl": _openssl_version(),
        "supports": {alg: supports_alg(alg) for alg in ALG_MAP},
    }


def supports_alg(alg: str) -> bool:
    if alg not in ALG_MAP or shutil.which("openssl") is None:
        return False
    p = subprocess.run(["openssl", "list", "-kem-algorithms"], capture_output=True, text=True)
    txt = (p.stdout + p.stderr)
    return ALG_MAP[alg] in txt


def _run(args, stdin=None):
    p = subprocess.run(args, input=stdin, capture_output=True)
    if p.returncode != 0:
        raise PQCBackendUnavailable((p.stderr or p.stdout).decode(errors="ignore")[:400])
    return p.stdout


def generate_keypair(alg: str) -> PQCKeyPair:
    if not supports_alg(alg):
        raise PQCBackendUnavailable("ML-KEM backend not available")
    with tempfile.TemporaryDirectory() as td:
        priv = os.path.join(td, "priv.pem")
        pub = os.path.join(td, "pub.pem")
        _run(["openssl", "genpkey", "-algorithm", ALG_MAP[alg], "-out", priv])
        _run(["openssl", "pkey", "-in", priv, "-pubout", "-out", pub])
        return PQCKeyPair(algorithm=alg, public_key=open(pub, "rb").read(), private_key=open(priv, "rb").read())


def encapsulate(alg: str, public_key: bytes):
    if not supports_alg(alg):
        raise PQCBackendUnavailable("ML-KEM backend not available")
    with tempfile.TemporaryDirectory() as td:
        pub = os.path.join(td, "pub.pem")
        ct = os.path.join(td, "ct.bin")
        ss = os.path.join(td, "ss.bin")
        open(pub, "wb").write(public_key)
        _run(["openssl", "pkeyutl", "-encap", "-inkey", pub, "-pubin", "-secret", ss, "-out", ct])
        return open(ct, "rb").read(), open(ss, "rb").read()


def decapsulate(alg: str, private_key: bytes, ciphertext: bytes):
    if not supports_alg(alg):
        raise PQCBackendUnavailable("ML-KEM backend not available")
    with tempfile.TemporaryDirectory() as td:
        priv = os.path.join(td, "priv.pem")
        ct = os.path.join(td, "ct.bin")
        ss = os.path.join(td, "ss.bin")
        open(priv, "wb").write(private_key)
        open(ct, "wb").write(ciphertext)
        _run(["openssl", "pkeyutl", "-decap", "-inkey", priv, "-in", ct, "-secret", ss])
        return open(ss, "rb").read()
