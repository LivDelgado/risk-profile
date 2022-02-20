from fastapi import APIRouter
from app.models.user import User

router = APIRouter()


@router.post("/insurances/", tags=["insurance"])
async def calculate_risk_insurance(user_information: User):
    return {
        "auto": "regular",
        "disability": "ineligible",
        "home": "economic",
        "life": "regular"
    }
