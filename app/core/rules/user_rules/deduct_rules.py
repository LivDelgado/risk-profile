from app.core.rules.rules import *
from app.core.rules.user_rules.user_rules import UserRule, UserIsMarried


class __DeductFromRiskScoreUserRule(DeductFromRiskScore, UserRule):
    pass


class DeductWhenYoungerThan30(__DeductFromRiskScoreUserRule):
    amount_to_deduct = 2

    def should_apply(self) -> bool:
        return self.user.age < 30


class DeductWhenBetween30and40(__DeductFromRiskScoreUserRule):
    def should_apply(self) -> bool:
        return 30 <= self.user.age <= 40


class DeductWhenIncomeOver200k(__DeductFromRiskScoreUserRule):
    def should_apply(self) -> bool:
        # assuming the income is already in thousands of dollars
        return self.user.income > 200000


class DeductWhenIsMarried(__DeductFromRiskScoreUserRule, UserIsMarried):
    pass
