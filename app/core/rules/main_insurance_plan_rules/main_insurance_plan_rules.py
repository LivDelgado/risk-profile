from typing import List

from app.core.rules.rules import Rule
from app.models.risk_profile import InsurancePlan


class MainInsurancePlansRules(Rule):
    def __init__(self, main_insurance_plans: List[InsurancePlan]):
        self.main_insurance_plans = main_insurance_plans
