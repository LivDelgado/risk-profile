import time
from typing import Tuple
from app.models.user import User, HouseOwnershipStatus, MarritalStatus
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


class IneligibleWhenNoIncome(Rule):
    def should_apply(self) -> bool:
        return self.user.income == 0

    def apply(self) -> Tuple[int, InsuranceProfile | None]:
        return self.base_score, InsuranceProfile.INELIGIBLE


class IneligibleWhenNoVehicle(Rule):
    def should_apply(self) -> bool:
        return not self.user.vehicle

    def apply(self) -> Tuple[int, InsuranceProfile | None]:
        return self.base_score, InsuranceProfile.INELIGIBLE


class IneligibleWhenNoHouse(Rule):
    def should_apply(self) -> bool:
        return not self.user.house

    def apply(self) -> Tuple[int, InsuranceProfile | None]:
        return self.base_score, InsuranceProfile.INELIGIBLE


class IneligibleWhenOlderThan60(Rule):
    def should_apply(self) -> bool:
        return self.user.age > 60

    def apply(self) -> Tuple[int, InsuranceProfile | None]:
        return self.base_score, InsuranceProfile.INELIGIBLE


class DeductWhenYoungerThan30(Rule):
    def should_apply(self) -> bool:
        return self.user.age < 30

    def apply(self) -> Tuple[int, InsuranceProfile | None]:
        self.add_to_score(-2)
        return self.base_score, None


class DeductWhenBetween30and40(Rule):
    def should_apply(self) -> bool:
        return 30 <= self.user.age <= 40

    def apply(self) -> Tuple[int, InsuranceProfile | None]:
        self.add_to_score(-1)
        return self.base_score, None


class DeductWhenIncomeOver200k(Rule):
    def should_apply(self) -> bool:
        # assuming the income is already in thousands of dollars
        return self.user.income > 200

    def apply(self) -> Tuple[int, InsuranceProfile | None]:
        self.add_to_score(-1)
        return self.base_score, None


class AddWhenHouseIsMortgaged(Rule):
    def should_apply(self) -> bool:
        return self.user.house and self.user.house.ownership_status == HouseOwnershipStatus.MORTGAGED

    def apply(self) -> Tuple[int, InsuranceProfile | None]:
        self.add_to_score(1)
        return self.base_score, None


class AddWhenHasDependents(Rule):
    def should_apply(self) -> bool:
        return self.user.dependents > 0

    def apply(self) -> Tuple[int, InsuranceProfile | None]:
        self.add_to_score(1)
        return self.base_score, None


class UserIsMarried(Rule):
    def should_apply(self) -> bool:
        return self.user.marital_status == MarritalStatus.MARRIED


class DeductWhenIsMarried(UserIsMarried):
    def apply(self) -> Tuple[int, InsuranceProfile | None]:
        self.add_to_score(-1)
        return self.base_score, None


class AddWhenIsMarried(UserIsMarried):
    def apply(self) -> Tuple[int, InsuranceProfile | None]:
        self.add_to_score(1)
        return self.base_score, None


class AddWhenVehicleIsNew(Rule):
    def should_apply(self) -> bool:
        max_age = 5
        current_year = int(time.strftime("%Y"))
        return self.user.vehicle and self.user.vehicle.year and self.user.vehicle.year > (current_year - max_age)

    def apply(self) -> Tuple[int, InsuranceProfile | None]:
        self.add_to_score(1)
        return self.base_score, None
