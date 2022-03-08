from pydantic import BaseModel
from enum import Enum


class InsurancePlan(Enum):
    INELIGIBLE = "ineligible"
    REGULAR = "regular"
    ECONOMIC = "economic"
    RESPONSIBLE = "responsible"


class InsurancePlanRecommendation(BaseModel):
    auto: InsurancePlan
    disability: InsurancePlan
    home: InsurancePlan | None
    renters: InsurancePlan | None
    life: InsurancePlan
    umbrella: InsurancePlan
