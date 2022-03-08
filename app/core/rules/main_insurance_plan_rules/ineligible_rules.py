from app.core.rules.main_insurance_plan_rules.main_insurance_plan_rules import (
    MainInsurancePlansRules,
)
from app.core.rules.rules import Ineligible
from app.models.risk_profile import InsurancePlan


class __IneligibleMainInsurancePlanRule(Ineligible, MainInsurancePlansRules):
    pass


class IneligibleWhenNoEconomicMainPlan(__IneligibleMainInsurancePlanRule):
    def should_apply(self) -> bool:
        return all(
            insurance_plan != InsurancePlan.ECONOMIC
            for insurance_plan in self.main_insurance_plans
        )
