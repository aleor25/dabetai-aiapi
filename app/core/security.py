from datetime import datetime, timedelta
from typing import Optional, Dict, Any

try:
    from passlib.context import CryptContext
except ImportError as e:
    raise ImportError(
        "passlib no está instalado. Ejecuta: .\\.venv\\Scripts\\python.exe -m pip install passlib"
    ) from e

try:
    from jose import jwt
except ImportError as e:
    raise ImportError(
        "python-jose no está instalado. Ejecuta: .\\.venv\\Scripts\\python.exe -m pip install python-jose[cryptography]"
    ) from e

from app.core.config import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

SECRET_KEY = getattr(settings, "SECRET_KEY", "change-me-in-production")
ALGORITHM = getattr(settings, "ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7))


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# alias para compatibilidad con código existente
def get_password_hash(password: str) -> str:
    return hash_password(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    now = datetime.now()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": now})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("token_expired")
    except Exception:
        # jose raises different exceptions; normalize as invalid token
        raise ValueError("token_invalid")
