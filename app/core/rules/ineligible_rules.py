from .rules import *


class Ineligible(Rule):
    def apply(self, current_score) -> Tuple[int, InsurancePlan | None]:
        return current_score, InsurancePlan.INELIGIBLE


class IneligibleWhenLowIncomeAndHighRisk(Ineligible):
    def should_apply(self) -> bool:
        return self.user.income < 25000 and sum(self.user.risk_questions) == 0


class IneligibleWhenNoIncome(Ineligible):
    def should_apply(self) -> bool:
        return self.user.income == 0


class IneligibleWhenNoVehicle(Ineligible):
    def should_apply(self) -> bool:
        return not self.user.vehicle


class IneligibleWhenNoHouse(Ineligible):
    def should_apply(self) -> bool:
        return not self.user.house


class IneligibleWhenOlderThan60(Ineligible):
    def should_apply(self) -> bool:
        return self.user.age > 60
