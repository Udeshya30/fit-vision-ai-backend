from pydantic import BaseModel
from typing import Optional

class OnboardingRequest(BaseModel):
    age: int
    height: float
    weight: float
    lifestyle: str
    goal: str
