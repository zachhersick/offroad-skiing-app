from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.models.domain import Mode, Profile, User
from app.schemas.auth import SignUpRequest


async def register_user(session: AsyncSession, payload: SignUpRequest) -> User:
    user = User(email=payload.email, password_hash=hash_password(payload.password))
    session.add(user)
    await session.flush()
    profile = Profile(
        user_id=user.id,
        display_name=payload.display_name,
        mode=Mode(payload.mode),
        home_region=payload.home_region,
        preferred_terrain=[],
        details={},
    )
    session.add(profile)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate_user(session: AsyncSession, email: str, password: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user and verify_password(password, user.password_hash):
        return user
    return None


def build_auth_payload(user: User) -> dict[str, str]:
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }
