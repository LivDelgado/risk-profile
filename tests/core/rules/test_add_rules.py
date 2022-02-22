from app.core.rules.add_rules import *
from app.models.user import *
import time

user = User(
    age=20,
    dependents=2,
    income=50,
    marital_status=MaritalStatus.MARRIED,
    risk_questions=[True, False, False],
)

base_score = 0


def test_apply_add_to_risk_score():
    rule = AddToRiskScore(user)
    new_score, plan = rule.apply(base_score)
    assert plan is None
    assert new_score == 1

    rule.amount_to_add = 3
    new_score, plan = rule.apply(new_score)
    assert plan is None
    assert new_score == 4


def test_house_mortgaged_rule_should_not_apply_no_house():
    user.house = None
    rule = AddWhenHouseIsMortgaged(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_house_mortgaged_rule_should_apply():
    user.house = House(ownership_status=HouseOwnershipStatus.MORTGAGED)
    rule = AddWhenHouseIsMortgaged(user)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_house_mortgaged_rule_should_not_apply_house_owned():
    user.house = House(ownership_status=HouseOwnershipStatus.OWNED)
    rule = AddWhenHouseIsMortgaged(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_dependents_rule_should_not_apply_no_dependents():
    user.dependents = 0
    rule = AddWhenHasDependents(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_dependents_rule_should_apply_has_dependents():
    user.dependents = 1
    rule = AddWhenHasDependents(user)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_marital_status_rule_should_not_apply_user_single():
    user.marital_status = MaritalStatus.SINGLE
    rule = AddWhenIsMarried(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_marital_status_rule_should_apply_user_married():
    user.marital_status = MaritalStatus.MARRIED
    rule = AddWhenIsMarried(user)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_new_vehicle_rule_should_not_apply_old_vehicle():
    user.vehicle = Vehicle(year=1890)
    rule = AddWhenVehicleIsNew(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_new_vehicle_rule_should_not_apply_vehicle_six_years():
    car_year = int(time.strftime("%Y")) - 6
    user.vehicle = Vehicle(year=car_year)
    rule = AddWhenVehicleIsNew(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_new_vehicle_rule_should_apply_vehicle_produced_five_years_ago():
    car_year = int(time.strftime("%Y")) - 5
    user.vehicle = Vehicle(year=car_year)
    rule = AddWhenVehicleIsNew(user)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_new_vehicle_rule_should_apply_vehicle_produced_less_than_five_years_ago():
    car_year = int(time.strftime("%Y")) - 2
    user.vehicle = Vehicle(year=car_year)
    rule = AddWhenVehicleIsNew(user)
    should_apply = rule.should_apply()
    assert should_apply is True
