from fastapi import APIRouter, HTTPException
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
    create_reset_token,
    hash_token,
    verify_token,
)

from app.email_service import send_reset_password_email

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
async def signup(data: SignupRequest):
    if await users_collection.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = create_user(
        email=data.email,
        password_hash=hash_password(data.password),
        name=data.name,
    )
    await users_collection.insert_one(user)

    return {"access_token": create_access_token(data.email)}

@router.post("/login")
async def login(data: LoginRequest):
    user = await users_collection.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": create_access_token(user["email"])}

@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest):
    user = await users_collection.find_one({"email": data.email})

    # IMPORTANT: Always return success (avoid user enumeration)
    if not user:
        return {"success": True}

    token = create_reset_token()
    token_hash = hash_token(token)

    await users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "reset_token_hash": token_hash,
                "reset_token_expiry": datetime.utcnow()
                + timedelta(minutes=30),
            }
        },
    )

    send_reset_password_email(data.email, token)
    return {"success": True}

@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest):
    user = await users_collection.find_one(
        {
            "reset_token_expiry": {"$gt": datetime.utcnow()},
        }
    )

    if not user or not verify_token(
        data.token, user.get("reset_token_hash", "")
    ):
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    await users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "password_hash": hash_password(data.new_password),
            },
            "$unset": {
                "reset_token_hash": "",
                "reset_token_expiry": "",
            },
        },
    )

    return {"success": True}
