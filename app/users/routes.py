from fastapi import APIRouter, Depends, HTTPException
from app.users.schemas import OnboardingRequest
from app.database import users_collection
from app.auth.deps import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/onboarding")
async def complete_onboarding(
    data: OnboardingRequest,
    user=Depends(get_current_user),
):
    await users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "profile.age": data.age,
                "profile.height": data.height,
                "profile.weight": data.weight,
                "profile.lifestyle": data.lifestyle,
                "profile.goal": data.goal,
                "onboarding_completed": True,
            }
        },
    )

    return {"success": True}



@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    return {
        "email": user["email"],
        "profile": user["profile"],
        "onboarding_completed": user.get("onboarding_completed", False),
    }
