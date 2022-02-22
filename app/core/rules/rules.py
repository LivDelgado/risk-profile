from typing import Tuple
from app.models.user import User, MaritalStatus
from app.models.risk_profile import InsurancePlan


class Rule:
    def __init__(self, user: User):
        self.user = user

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


class UserIsMarried(Rule):
    def should_apply(self) -> bool:
        return self.user.marital_status == MaritalStatus.MARRIED
