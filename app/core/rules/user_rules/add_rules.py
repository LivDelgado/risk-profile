import time
from app.core.rules.rules import *
from app.core.rules.user_rules.user_rules import UserIsMarried, UserRule
from app.models.user import HouseOwnershipStatus


class __AddToRiskScoreUserRule(AddToRiskScore, UserRule):
    pass


class AddWhenHasDependents(__AddToRiskScoreUserRule):
    def should_apply(self) -> bool:
        return self.user.dependents > 0


class AddWhenIsMarried(AddToRiskScore, UserIsMarried):
    pass


class AddWhenVehicleIsNew(__AddToRiskScoreUserRule):
    def should_apply(self) -> bool:
        max_age = 5
        current_year = int(time.strftime("%Y"))
        min_year = current_year - max_age
        return self.user.vehicle is not None and self.user.vehicle.year >= min_year
