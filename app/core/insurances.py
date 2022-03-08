from typing import List, Optional

from app.core.rules.main_insurance_plan_rules.ineligible_rules import (
    IneligibleWhenNoEconomicMainPlan,
)
from app.core.rules.user_rules.ineligible_rules import *
from app.core.rules.user_rules.deduct_rules import *
from app.core.rules.user_rules.add_rules import *
from app.models.user import User


class Insurance:
    def __init__(self, user: User, base_score: int, rules: List[Rule]):
        base_rules = [
            DeductWhenYoungerThan30(user),
            DeductWhenBetween30and40(user),
            DeductWhenIncomeOver200k(user),
            IneligibleWhenLowIncomeAndHighRisk(user),
        ]
        self.user = user
        self.base_score = base_score
        self.rules_list = base_rules
        self.rules_list.extend(rules)

    @staticmethod
    def determine_final_profile(score: int) -> InsurancePlan:
        """
        Determines insurance plan based on final risk score

        :param score: score to be analysed
        :return: insurance plan based on risk score
        """
        if score <= 0:
            return InsurancePlan.ECONOMIC
        elif score < 3:
            return InsurancePlan.REGULAR
        else:
            return InsurancePlan.RESPONSIBLE

    def recommend_plan_when_applicable(self) -> Optional[InsurancePlan]:
        if self.is_recommendable():
            return self.get_insurance_plan_recommendation()

    def is_recommendable(self) -> bool:
        return True

    def get_insurance_plan_recommendation(self) -> InsurancePlan:
        """
        Suggest plan based on the risk profile rules for the insurance line

        :return: insurance plan based on risk profile
        """
        for rule in self.rules_list:
            if rule.should_apply():
                current_score, final_profile = rule.apply(self.base_score)

                # updates the score
                self.base_score = current_score

                if final_profile:  # this means that it is already a final result
                    return final_profile

        return self.determine_final_profile(self.base_score)


class SecondaryInsurance(Insurance):
    def __init__(
        self,
        user: User,
        base_score: int,
        main_insurances: List[InsurancePlan],
        rules: List[Rule],
    ):
        self.main_insurances = main_insurances
        super().__init__(user, base_score, rules)


class Umbrella(SecondaryInsurance):
    def __init__(
        self, user: User, base_score: int, main_insurances: List[InsurancePlan]
    ):
        rules_list = [IneligibleWhenNoEconomicMainPlan(main_insurances)]
        super().__init__(user, base_score, main_insurances, rules_list)


class Disability(Insurance):
    def __init__(self, user: User, base_score: int):
        rules_list = [
            IneligibleWhenNoIncome(user),
            IneligibleWhenOlderThan60(user),
            AddWhenHasDependents(user),
            DeductWhenIsMarried(user),
        ]
        super().__init__(user, base_score, rules_list)


class Auto(Insurance):
    def __init__(self, user: User, base_score: int):
        rules_list = [
            IneligibleWhenNoVehicle(user),
            AddWhenVehicleIsNew(user),
        ]
        super().__init__(user, base_score, rules_list)


class House(Insurance):
    def __init__(self, user: User, base_score: int):
        rules_list = [
            IneligibleWhenNoHouse(user),
        ]
        super().__init__(user, base_score, rules_list)


class Home(House):
    def is_recommendable(self) -> bool:
        return (
            self.user.house is None
            or self.user.house.ownership_status == HouseOwnershipStatus.OWNED
        )


class Renters(House):
    def is_recommendable(self) -> bool:
        return (
            self.user.house is None
            or self.user.house.ownership_status == HouseOwnershipStatus.RENTED
        )


class Life(Insurance):
    def __init__(self, user: User, base_score: int):
        rules_list = [
            IneligibleWhenOlderThan60(user),
            AddWhenHasDependents(user),
            AddWhenIsMarried(user),
        ]
        super().__init__(user, base_score, rules_list)
