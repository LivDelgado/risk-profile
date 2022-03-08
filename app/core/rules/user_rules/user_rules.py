from app.core.rules.rules import Rule
from app.models.user import User, MaritalStatus


class UserRule(Rule):
    def __init__(self, user: User):
        self.user = user


class UserIsMarried(UserRule):
    def should_apply(self) -> bool:
        return self.user.marital_status == MaritalStatus.MARRIED
