import hashlib
import hmac
import os
import base64

# Pure-Python password hashing using PBKDF2-HMAC-SHA256
# Replaces passlib+bcrypt which is blocked by Device Guard DLL policy

_ITERATIONS = 260000
_ALGORITHM = "sha256"


def hash_password(plain: str) -> str:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(_ALGORITHM, plain.encode(), salt, _ITERATIONS)
    return "pbkdf2$" + base64.b64encode(salt).decode() + "$" + base64.b64encode(key).decode()


def verify_password(plain: str, hashed: str) -> bool:
    try:
        if not hashed.startswith("pbkdf2$"):
            # Legacy bcrypt hash — cannot verify, return False
            return False
        _, salt_b64, key_b64 = hashed.split("$")
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(key_b64)
        actual = hashlib.pbkdf2_hmac(_ALGORITHM, plain.encode(), salt, _ITERATIONS)
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False
