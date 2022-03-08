from app.core.rules.deduct_rules import *
from app.models.user import *

user = User(
    age=20,
    dependents=2,
    income=50,
    marital_status=MaritalStatus.MARRIED,
    risk_questions=[True, False, False],
)

base_score = 0


def test_apply_deduct_from_risk_score():
    rule = DeductFromRiskScore(user)
    new_score, plan = rule.apply(base_score)
    assert plan is None
    assert new_score == -1

    rule.amount_to_deduct = 3
    new_score, plan = rule.apply(new_score)
    assert plan is None
    assert new_score == -4


def test_younger_than_30_should_apply():
    user.age = 20
    rule = DeductWhenYoungerThan30(user)
    should_apply = rule.should_apply()
    assert should_apply is True
    new_score, plan = rule.apply(base_score)
    assert new_score == base_score - 2


def test_younger_than_30_should_not_apply():
    user.age = 30
    rule = DeductWhenYoungerThan30(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_age_between_30_and_40_should_apply_30():
    user.age = 30
    rule = DeductWhenBetween30and40(user)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_age_between_30_and_40_should_apply_40():
    user.age = 40
    rule = DeductWhenBetween30and40(user)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_age_between_30_and_40_should_apply_35():
    user.age = 35
    rule = DeductWhenBetween30and40(user)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_age_between_30_and_40_should_not_apply_younger():
    user.age = 29
    rule = DeductWhenBetween30and40(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_age_between_30_and_40_should_not_apply_older():
    user.age = 41
    rule = DeductWhenBetween30and40(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_income_over_200k_should_apply():
    user.income = 201000
    rule = DeductWhenIncomeOver200k(user)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_income_over_200k_should_not_apply_exact():
    user.income = 200
    rule = DeductWhenIncomeOver200k(user)
    should_apply = rule.should_apply()
    assert should_apply is False


def test_deduct_when_married_should_apply():
    user.marital_status = MaritalStatus.MARRIED
    rule = DeductWhenIsMarried(user)
    should_apply = rule.should_apply()
    assert should_apply is True


def test_deduct_when_married_should_not_apply_single():
    user.marital_status = MaritalStatus.SINGLE
    rule = DeductWhenIsMarried(user)
    should_apply = rule.should_apply()
    assert should_apply is False
