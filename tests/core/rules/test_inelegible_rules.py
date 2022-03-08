from app.core.rules.user_rules.ineligible_rules import *
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
    rule = Ineligible()
    new_score, plan = rule.apply(base_score)
    assert plan is InsurancePlan.INELIGIBLE
    assert new_score == base_score


def test_ineligible_no_income_should_apply():
    user.income = 0
    rule = IneligibleWhenNoIncome(user)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_ineligible_no_income_should_not_apply():
    user.income = 10
    rule = IneligibleWhenNoIncome(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_ineligible_no_vehicle_should_apply():
    user.vehicle = None
    rule = IneligibleWhenNoVehicle(user)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_ineligible_no_vehicle_should_not_apply():
    user.vehicle = Vehicle(year=2000)
    rule = IneligibleWhenNoVehicle(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_ineligible_no_house_should_apply():
    user.house = None
    rule = IneligibleWhenNoHouse(user)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_ineligible_no_house_should_not_apply():
    user.house = House(ownership_status=HouseOwnershipStatus.OWNED)
    rule = IneligibleWhenNoHouse(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_ineligible_when_older_than_60_should_apply():
    user.age = 61
    rule = IneligibleWhenOlderThan60(user)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_ineligible_when_older_than_60_should_not_apply_exact_age():
    user.age = 60
    rule = IneligibleWhenOlderThan60(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_ineligible_when_older_than_60_should_not_apply_younger():
    user.age = 59
    rule = IneligibleWhenOlderThan60(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_ineligible_when_low_income_and_high_risk_should_apply():
    user.income = 2000
    user.risk_questions = [False, False, False]
    rule = IneligibleWhenLowIncomeAndHighRisk(user)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_ineligible_when_low_income_and_high_risk_should_not_apply_risk_question():
    user.income = 2000
    user.risk_questions = [False, False, True]
    rule = IneligibleWhenLowIncomeAndHighRisk(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_ineligible_when_low_income_and_high_risk_should_not_apply_income_is_higher():
    user.income = 25000
    user.risk_questions = [False, False, False]
    rule = IneligibleWhenLowIncomeAndHighRisk(user)
    should_apply = rule.should_apply()
    assert should_apply is False
