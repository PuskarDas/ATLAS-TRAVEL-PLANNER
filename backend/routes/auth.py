"""Authentication routes."""

from database.store import store
from fastapi import APIRouter, HTTPException, status
from models.schemas import LoginRequest, TokenResponse, UserCreate
from pydantic import BaseModel
from utils.auth_utils import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    public_user,
    verify_password,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post(
    "/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
async def register(payload: UserCreate):
    if any(user["email"] == payload.email for user in store.users.values()):
        raise HTTPException(status_code=409, detail="Email already registered")
    if any(user["username"] == payload.username for user in store.users.values()):
        raise HTTPException(status_code=409, detail="Username already registered")

    user = store.insert(
        "users",
        {
            "username": payload.username,
            "email": payload.email,
            "hashed_password": hash_password(payload.password),
            "first_name": payload.first_name,
            "last_name": payload.last_name,
            "profile_picture": None,
            "is_active": True,
        },
    )
    return {
        "access_token": create_access_token(user["id"]),
        "refresh_token": create_refresh_token(user["id"]),
        "user": public_user(user),
    }


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    user = next(
        (item for item in store.users.values() if item["email"] == payload.email), None
    )
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {
        "access_token": create_access_token(user["id"]),
        "refresh_token": create_refresh_token(user["id"]),
        "user": public_user(user),
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest):
    token_payload = decode_token(payload.refresh_token)
    if token_payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    token_id = token_payload.get("jti")
    user_id = int(token_payload["sub"])
    if store.refresh_tokens.get(token_id) != user_id:
        raise HTTPException(status_code=401, detail="Refresh token revoked")
    user = store.get("users", user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return {
        "access_token": create_access_token(user_id),
        "refresh_token": create_refresh_token(user_id),
        "user": public_user(user),
    }


@router.post("/logout")
async def logout(payload: RefreshRequest):
    token_payload = decode_token(payload.refresh_token)
    token_id = token_payload.get("jti")
    store.refresh_tokens.pop(token_id, None)
    return {"message": "Logged out"}
