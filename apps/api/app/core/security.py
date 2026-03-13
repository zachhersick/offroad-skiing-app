from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from argon2 import PasswordHasher

from .config import get_settings


password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except Exception:
        return False


def create_token(subject: str, token_type: str, minutes: int, secret: str) -> str:
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "exp": datetime.now(UTC) + timedelta(minutes=minutes),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def create_access_token(subject: str) -> str:
    return create_token(subject, "access", 30, get_settings().jwt_secret)


def create_refresh_token(subject: str) -> str:
    return create_token(subject, "refresh", 60 * 24 * 7, get_settings().jwt_refresh_secret)


def decode_token(token: str, *, refresh: bool = False) -> dict[str, Any]:
    secret = get_settings().jwt_refresh_secret if refresh else get_settings().jwt_secret
    return jwt.decode(token, secret, algorithms=["HS256"])

