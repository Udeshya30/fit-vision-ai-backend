from fastapi import APIRouter, HTTPException, Response, Request
from datetime import datetime, timedelta

from app.database import users_collection
from app.models import create_user
from app.schemas import (
    SignupRequest,
    LoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.auth.utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    hash_token,
    verify_token,
)
from app.email_service import send_reset_password_email

router = APIRouter(prefix="/auth", tags=["Auth"])

COOKIE_SETTINGS = {
    "httponly": True,
    "secure": False,   # set True in production (HTTPS)
    "samesite": "lax",
    "path": "/",
}


@router.post("/signup")
async def signup(data: SignupRequest, response: Response):
    if await users_collection.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    refresh_token = create_refresh_token()

    user = create_user(
        email=data.email,
        password_hash=hash_password(data.password),
        name=data.name,
    )

    user["refresh_token_hash"] = hash_token(refresh_token)
    await users_collection.insert_one(user)

    response.set_cookie(
        "access_token",
        create_access_token(data.email),
        max_age=15 * 60,
        **COOKIE_SETTINGS,
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        max_age=7 * 24 * 60 * 60,
        **COOKIE_SETTINGS,
    )

    return {"success": True}


@router.post("/login")
async def login(data: LoginRequest, response: Response):
    user = await users_collection.find_one({"email": data.email})

    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    refresh_token = create_refresh_token()

    await users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "refresh_token_hash": hash_token(refresh_token),
                "last_login": datetime.utcnow(),
            }
        },
    )

    response.set_cookie(
        "access_token",
        create_access_token(user["email"]),
        max_age=15 * 60,
        **COOKIE_SETTINGS,
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        max_age=7 * 24 * 60 * 60,
        **COOKIE_SETTINGS,
    )

    return {"success": True}


@router.post("/refresh")
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    user = await users_collection.find_one(
        {"refresh_token_hash": hash_token(refresh_token)}
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_refresh = create_refresh_token()

    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"refresh_token_hash": hash_token(new_refresh)}},
    )

    response.set_cookie(
        "access_token",
        create_access_token(user["email"]),
        max_age=15 * 60,
        **COOKIE_SETTINGS,
    )
    response.set_cookie(
        "refresh_token",
        new_refresh,
        max_age=7 * 24 * 60 * 60,
        **COOKIE_SETTINGS,
    )

    return {"success": True}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"success": True}
