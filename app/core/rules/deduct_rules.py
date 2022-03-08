from .rules import *


class DeductFromRiskScore(Rule):
    amount_to_deduct = 1

    def apply(self, current_score) -> Tuple[int, InsurancePlan | None]:
        return current_score - self.amount_to_deduct, None


class DeductWhenYoungerThan30(DeductFromRiskScore):
    amount_to_deduct = 2

    def should_apply(self) -> bool:
        return self.user.age < 30


class DeductWhenBetween30and40(DeductFromRiskScore):
    def should_apply(self) -> bool:
        return 30 <= self.user.age <= 40


class DeductWhenIncomeOver200k(DeductFromRiskScore):
    def should_apply(self) -> bool:
        # assuming the income is already in thousands of dollars
        return self.user.income > 200000


class DeductWhenIsMarried(DeductFromRiskScore, UserIsMarried):
    pass
