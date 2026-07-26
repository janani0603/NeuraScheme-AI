from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from app.config.settings import settings


def create_access_token(user_id: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> str:
    """Returns user_id (sub) or raises JWTError."""
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    user_id: str = payload.get("sub")
    if user_id is None:
        raise JWTError("Missing subject in token")
    return user_id
