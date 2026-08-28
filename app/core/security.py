# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import jwt, JWTError

from app.core.config import settings

def hash_password(password: str) -> str:
    """Takes a plain password and returns a secure, irreversible hash of it."""
    # Bcrypt requires passwords to be converted to bytes first
    password_bytes = password.encode('utf-8')
    
    # Generate a secure salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # Return it as a normal string to save in the database
    return hashed_password_bytes.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks a login attempt's password against the stored hash."""
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Builds a signed JWT token containing the given data (usually the user's id/email).
    This token is what the client stores and sends back on every request to prove who they are."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Verifies a token's signature and expiry, and returns its contents if valid.
    Returns None if the token is invalid, tampered with, or expired."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None