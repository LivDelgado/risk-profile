from fastapi import APIRouter
from app.models.user import User
from app.models.risk_profile import InsurancePlanRecommendation

from app.core.risk_algorithm import calculate_risk_profile

router = APIRouter()


@router.post(
    "/risk-profiles/",
    tags=["risk profiles"],
    response_model=InsurancePlanRecommendation,
    response_model_exclude_none=True,
)
async def calculate_insurance_recommendation(
    user_information: User,
) -> InsurancePlanRecommendation:
    return calculate_risk_profile(user_information)
