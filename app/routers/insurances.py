from fastapi import APIRouter
from app.models.user import User

from app.core.risk_algorithm import calculate_risk_score

router = APIRouter()


@router.post("/insurances/", tags=["insurance"])
async def calculate_risk_insurance(user_information: User):
    return calculate_risk_score(user_information)
