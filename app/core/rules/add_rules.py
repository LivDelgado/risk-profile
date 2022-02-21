import time
from .rules import *
from app.models.user import HouseOwnershipStatus


class AddToRiskScore(Rule):
    amount_to_add = 1

    def apply(self) -> Tuple[int, InsurancePlan | None]:
        self.add_to_score(self.amount_to_add)
        return self.base_score, None


class AddWhenHouseIsMortgaged(AddToRiskScore):
    def should_apply(self) -> bool:
        return self.user.house is not None and self.user.house.ownership_status == HouseOwnershipStatus.MORTGAGED


class AddWhenHasDependents(AddToRiskScore):
    def should_apply(self) -> bool:
        return self.user.dependents > 0


class AddWhenIsMarried(AddToRiskScore, UserIsMarried):
    pass


class AddWhenVehicleIsNew(AddToRiskScore):
    def should_apply(self) -> bool:
        max_age = 5
        current_year = int(time.strftime("%Y"))
        min_year = current_year - max_age
        return self.user.vehicle is not None and self.user.vehicle.year >= min_year
