from pydantic import BaseModel
from enum import Enum


class InsuranceProfile(Enum):
    INELIGIBLE = "ineligible"
    REGULAR = "regular"
    ECONOMIC = "economic"
    RESPONSIBLE = "responsible"


class RiskProfile(BaseModel):
    auto: InsuranceProfile
    disability: InsuranceProfile
    home: InsuranceProfile
    life: InsuranceProfile
