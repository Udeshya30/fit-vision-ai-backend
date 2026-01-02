from fastapi import APIRouter, Depends
from app.auth.deps import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
async def dashboard_home(current_user=Depends(get_current_user)):
    return {
        "message": "Welcome to FitVisionAI Dashboard",
        "user": {
            "email": current_user["email"],
            "name": current_user["profile"]["name"],
        },
    }
