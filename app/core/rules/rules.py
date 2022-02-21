from typing import Tuple
from app.models.user import User, MaritalStatus
from app.models.risk_profile import InsurancePlan


class Rule:
    def __init__(self, user: User, base_score: int):
        self.user = user
        self.base_score = base_score

    def should_apply(self) -> bool:
        """
        Determines if rule should be applied to user

        :return: boolean with result of validation
        """
        return False

    def add_to_score(self, n) -> None:
        """
        Add 'n' to the risk score
        :param n: number to be added
        :return: nothing. it modifies an internal property.
        """
        self.base_score = self.base_score + n

    def apply(self) -> Tuple[int, InsurancePlan | None]:
        """
        Apply the rule to the user information
        :return: tuple with new score and optional final risk profile for the insurance
        """
        return self.base_score, None


class UserIsMarried(Rule):
    def should_apply(self) -> bool:
        return self.user.marital_status == MaritalStatus.MARRIED
