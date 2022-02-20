from typing import Tuple
from app.models.user import User, MarritalStatus
from app.models.risk_profile import InsuranceProfile


class Rule:
    def __init__(self, user: User, base_score: int):
        self.user = user
        self.base_score = base_score

    def should_apply(self) -> bool:
        return False

    def add_to_score(self, n) -> None:
        self.base_score = self.base_score + n

    def apply(self) -> Tuple[int, InsuranceProfile | None]:
        return self.base_score, None


class UserIsMarried(Rule):
    def should_apply(self) -> bool:
        return self.user.marital_status == MarritalStatus.MARRIED

