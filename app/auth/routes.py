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
from app.config import FRONTEND_BASE_URL
from app.email_service import send_reset_password_email, send_welcome_email, send_password_changed_email

router = APIRouter(prefix="/auth", tags=["Auth"])

COOKIE_SETTINGS = {
    "httponly": True,
    "secure": True,   # set True in production (HTTPS)
    # "samesite": "lax",
    "samesite": "none",
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

    # Set cookies
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

    # SEND WELCOME EMAIL (NON-BLOCKING)
    try:
        send_welcome_email(data.email, data.name)
    except Exception as e:
        print("Welcome email failed:", e)

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


# @router.post("/logout")
# async def logout(response: Response):
#     response.delete_cookie("access_token")
#     response.delete_cookie("refresh_token")
#     return {"success": True}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        samesite="none",
        secure=True,
    )
    response.delete_cookie(
        key="refresh_token",
        path="/",
        samesite="none",
        secure=True,
    )
    return {"success": True}



@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest):
    user = await users_collection.find_one({"email": data.email})
    if not user:
        return {"success": True}  # Do not leak info

    token = create_refresh_token()
    hashed = hash_token(token)

    await users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "reset_password_token": hashed,
                "reset_password_expires": datetime.utcnow() + timedelta(minutes=15),
            }
        },
    )

    reset_link = f"{FRONTEND_BASE_URL}/reset-password/{token}"

    send_reset_password_email(data.email, reset_link)

    return {"success": True}


@router.post("/reset-password/{token}")
async def reset_password(token: str, data: ResetPasswordRequest):
    hashed = hash_token(token)

    user = await users_collection.find_one(
        {
            "reset_password_token": hashed,
            "reset_password_expires": {"$gt": datetime.utcnow()},
        }
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset link",
        )

    await users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "password_hash": hash_password(data.password),
            },
            "$unset": {
                "reset_password_token": "",
                "reset_password_expires": "",
            },
        },
    )

    # SEND PASSWORD-CHANGED EMAIL (NON-BLOCKING)
    # try:
    #     send_password_changed_email(
    #         user["email"],
    #         user.get("profile", {}).get("name", "there"),
    #     )
    # except Exception as e:
    #     print("Password changed email failed:", e)
        
    try:
        print("Sending password changed email...")
        send_password_changed_email(
            user["email"],
            user.get("profile", {}).get("name", "there"),
        )
        print("Password changed email sent")
    except Exception as e:
        print("Password changed email failed:", repr(e))


    return {"success": True}

