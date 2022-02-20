from .rules import *


class Ineligible(Rule):
    def apply(self) -> Tuple[int, InsuranceProfile | None]:
        return self.base_score, InsuranceProfile.INELIGIBLE


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
