from app.core.rules.rules import *
from app.core.rules.user_rules.user_rules import UserRule


class __IneligibleUserRule(Ineligible, UserRule):
    pass


class IneligibleWhenLowIncomeAndHighRisk(__IneligibleUserRule):
    def should_apply(self) -> bool:
        return self.user.income < 25000 and sum(self.user.risk_questions) == 0


class IneligibleWhenNoIncome(__IneligibleUserRule):
    def should_apply(self) -> bool:
        return self.user.income == 0


class IneligibleWhenNoVehicle(__IneligibleUserRule):
    def should_apply(self) -> bool:
        return not self.user.vehicle


class IneligibleWhenNoHouse(__IneligibleUserRule):
    def should_apply(self) -> bool:
        return not self.user.house


class IneligibleWhenOlderThan60(__IneligibleUserRule):
    def should_apply(self) -> bool:
        return self.user.age > 60
