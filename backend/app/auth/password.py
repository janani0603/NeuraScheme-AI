from passlib.context import CryptContext
import warnings

# Suppress passlib deprecation warning on newer bcrypt versions
warnings.filterwarnings("ignore", ".*bcrypt.*", category=DeprecationWarning)

_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return _ctx.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return _ctx.verify(plain, hashed)
