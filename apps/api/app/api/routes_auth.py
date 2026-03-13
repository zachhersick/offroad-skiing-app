from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.domain import Profile, User
from app.schemas.auth import SignInRequest, SignUpRequest, UserResponse
from app.services.auth import authenticate_user, build_auth_payload, register_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(payload: SignUpRequest, response: Response, db: AsyncSession = Depends(get_db)) -> UserResponse:
    existing = await db.execute(select(User).where(User.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await register_user(db, payload)
    profile = (await db.execute(select(Profile).where(Profile.user_id == user.id))).scalar_one()
    tokens = build_auth_payload(user)
    response.set_cookie("access_token", tokens["access_token"], httponly=True, samesite="lax")
    response.set_cookie("refresh_token", tokens["refresh_token"], httponly=True, samesite="lax")
    return UserResponse(id=user.id, email=user.email, display_name=profile.display_name, mode=profile.mode.value)


@router.post("/signin", response_model=UserResponse)
async def signin(payload: SignInRequest, response: Response, db: AsyncSession = Depends(get_db)) -> UserResponse:
    user = await authenticate_user(db, payload.email, payload.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    profile = (await db.execute(select(Profile).where(Profile.user_id == user.id))).scalar_one()
    tokens = build_auth_payload(user)
    response.set_cookie("access_token", tokens["access_token"], httponly=True, samesite="lax")
    response.set_cookie("refresh_token", tokens["refresh_token"], httponly=True, samesite="lax")
    return UserResponse(id=user.id, email=user.email, display_name=profile.display_name, mode=profile.mode.value)


@router.post("/signout", status_code=status.HTTP_204_NO_CONTENT)
async def signout(response: Response) -> Response:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@router.get("/me", response_model=UserResponse)
async def me(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> UserResponse:
    profile = (await db.execute(select(Profile).where(Profile.user_id == user.id))).scalar_one()
    return UserResponse(id=user.id, email=user.email, display_name=profile.display_name, mode=profile.mode.value)

