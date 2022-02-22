from app.core.rules.ineligible_rules import *
from app.models.user import *

user = User(
    age=20,
    dependents=2,
    income=50,
    marital_status=MaritalStatus.MARRIED,
    risk_questions=[True, False, False],
)

base_score = 0


def test_apply_ineligible():
    rule = Ineligible(user, base_score)
    new_score, plan = rule.apply()
    assert plan is InsurancePlan.INELIGIBLE
    assert new_score == base_score


def test_ineligible_no_income_should_apply():
    user.income = 0
    rule = IneligibleWhenNoIncome(user, base_score)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_ineligible_no_income_should_not_apply():
    user.income = 10
    rule = IneligibleWhenNoIncome(user, base_score)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_ineligible_no_vehicle_should_apply():
    user.vehicle = None
    rule = IneligibleWhenNoVehicle(user, base_score)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_ineligible_no_vehicle_should_not_apply():
    user.vehicle = Vehicle(year=2000)
    rule = IneligibleWhenNoVehicle(user, base_score)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_ineligible_no_house_should_apply():
    user.house = None
    rule = IneligibleWhenNoHouse(user, base_score)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_ineligible_no_house_should_not_apply():
    user.house = House(ownership_status=HouseOwnershipStatus.OWNED)
    rule = IneligibleWhenNoHouse(user, base_score)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_ineligible_when_older_than_60_should_apply():
    user.age = 61
    rule = IneligibleWhenOlderThan60(user, base_score)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_ineligible_when_older_than_60_should_not_apply_exact_age():
    user.age = 60
    rule = IneligibleWhenOlderThan60(user, base_score)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_ineligible_when_older_than_60_should_not_apply_younger():
    user.age = 59
    rule = IneligibleWhenOlderThan60(user, base_score)
    should_apply = rule.should_apply()
    assert should_apply is False
