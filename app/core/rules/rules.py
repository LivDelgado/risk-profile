from typing import Tuple
from app.models.risk_profile import InsurancePlan


class Rule:
    def should_apply(self) -> bool:
        """
        Determines if rule should be applied to user

        :return: boolean with result of validation
        """
        return False

    def apply(self, current_score) -> Tuple[int, InsurancePlan | None]:
        """
        Apply the rule to the user information
        :return: tuple with new score and optional final risk profile for the insurance
        """
        return current_score, None


class Ineligible(Rule):
    def apply(self, current_score) -> Tuple[int, InsurancePlan | None]:
        return current_score, InsurancePlan.INELIGIBLE


class AddToRiskScore(Rule):
    amount_to_add = 1

    def apply(self, current_score) -> Tuple[int, InsurancePlan | None]:
        return current_score + self.amount_to_add, None


class DeductFromRiskScore(Rule):
    amount_to_deduct = 1

    def apply(self, current_score) -> Tuple[int, InsurancePlan | None]:
        return current_score - self.amount_to_deduct, None
