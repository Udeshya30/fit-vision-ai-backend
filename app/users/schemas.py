from pydantic import BaseModel, Field

class OnboardingRequest(BaseModel):
    age: int = Field(..., ge=10, le=100)
    weight: float = Field(..., ge=30, le=300)
    height: float = Field(..., ge=100, le=250)
    lifestyle: str
    goal: str
