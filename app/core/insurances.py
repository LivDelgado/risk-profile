from typing import List
from .rules.ineligible_rules import *
from .rules.deduct_rules import *
from .rules.add_rules import *


class Insurance:
    def __init__(self, user: User, base_score: int, rules_list: List[Rule]):
        self.user = user
        self.base_score = base_score
        self.rules_list = rules_list

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

    def get_insurance_plan_recommendation(self) -> InsurancePlan:
        """
        Suggest plan based on the risk profile rules for the insurance line

        :return: insurance plan based on risk profile
        """
        for rule in self.rules_list:
            if rule.should_apply():
                current_score, final_profile = rule.apply()

                # updates the score
                self.base_score = current_score

                if final_profile:  # this means that it is already a final result
                    return final_profile

        return self.determine_final_profile(self.base_score)


class Disability(Insurance):
    def __init__(self, user: User, base_score: int):
        rules_list = [
            IneligibleWhenNoIncome(user, base_score),
            IneligibleWhenOlderThan60(user, base_score),
            DeductWhenYoungerThan30(user, base_score),
            DeductWhenBetween30and40(user, base_score),
            DeductWhenIncomeOver200k(user, base_score),
            AddWhenHouseIsMortgaged(user, base_score),
            AddWhenHasDependents(user, base_score),
            DeductWhenIsMarried(user, base_score),
        ]
        super().__init__(user, base_score, rules_list)


class Auto(Insurance):
    def __init__(self, user: User, base_score: int):
        rules_list = [
            IneligibleWhenNoVehicle(user, base_score),
            DeductWhenYoungerThan30(user, base_score),
            DeductWhenBetween30and40(user, base_score),
            DeductWhenIncomeOver200k(user, base_score),
            AddWhenVehicleIsNew(user, base_score),
        ]
        super().__init__(user, base_score, rules_list)


class Home(Insurance):
    def __init__(self, user: User, base_score: int):
        rules_list = [
            IneligibleWhenNoHouse(user, base_score),
            DeductWhenYoungerThan30(user, base_score),
            DeductWhenBetween30and40(user, base_score),
            DeductWhenIncomeOver200k(user, base_score),
            AddWhenHouseIsMortgaged(user, base_score),
        ]
        super().__init__(user, base_score, rules_list)


class Life(Insurance):
    def __init__(self, user: User, base_score: int):
        rules_list = [
            IneligibleWhenOlderThan60(user, base_score),
            DeductWhenYoungerThan30(user, base_score),
            DeductWhenBetween30and40(user, base_score),
            DeductWhenIncomeOver200k(user, base_score),
            AddWhenHasDependents(user, base_score),
            AddWhenIsMarried(user, base_score),
        ]
        super().__init__(user, base_score, rules_list)
