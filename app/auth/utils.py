import secrets
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from app.config import JWT_SECRET, JWT_ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 15
RESET_TOKEN_EXPIRE_MINUTES = 30

def _normalize_password(password: str) -> str:
    pw = password.encode("utf-8")
    return pw[:72].decode("utf-8", errors="ignore") if len(pw) > 72 else password

def hash_password(password: str) -> str:
    return pwd_context.hash(_normalize_password(password))

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(_normalize_password(password), hashed)

def create_access_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def create_reset_token() -> str:
    return secrets.token_urlsafe(48)

def hash_token(token: str) -> str:
    return pwd_context.hash(token)

def verify_token(token: str, hashed: str) -> bool:
    return pwd_context.verify(token, hashed)
