from fastapi import APIRouter, Depends, HTTPException
from app.users.schemas import OnboardingRequest
from app.database import users_collection
from app.auth.deps import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.put("/onboarding")
async def complete_onboarding(
    data: OnboardingRequest,
    current_user=Depends(get_current_user),
):
    await users_collection.update_one(
        {"_id": current_user["_id"]},
        {
            "$set": {
                "profile.age": data.age,
                "profile.weight": data.weight,
                "profile.height": data.height,
                "profile.lifestyle": data.lifestyle,
                "profile.goal": data.goal,
                "onboarding_completed": True,
            }
        },
    )

    return {"success": True}
