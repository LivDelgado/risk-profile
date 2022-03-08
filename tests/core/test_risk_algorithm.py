from app.core.risk_algorithm import *
from app.models.risk_profile import InsurancePlan
from app.models.user import *


def test_risk_algorithm_all_ineligible():
    user = User(
        age=61,
        dependents=2,
        income=0,
        marital_status=MaritalStatus.MARRIED,
        risk_questions=[True, False, False],
    )

    result = calculate_risk_profile(user=user)
    assert result.auto == InsurancePlan.INELIGIBLE
    assert result.home == InsurancePlan.INELIGIBLE
    assert result.disability == InsurancePlan.INELIGIBLE
    assert result.life == InsurancePlan.INELIGIBLE
    assert result.renters == InsurancePlan.INELIGIBLE
    assert result.umbrella == InsurancePlan.INELIGIBLE


def test_risk_algorithm_user_married_younger_than_30_large_income():
    user = User(
        age=29,
        dependents=2,
        income=300000,
        marital_status=MaritalStatus.MARRIED,
        risk_questions=[True, True, True],
        house=House(ownership_status=HouseOwnershipStatus.OWNED),
        vehicle=Vehicle(year=int(time.strftime("%Y"))),
    )

    # < 30y -> remove 2 from all
    # income > 200k -> remove 1 from all
    # has dependents -> add 1 to disability and life
    # married -> remove 1 from disability, add one to life
    # new vehicle -> add 1 to auto

    # base score is 3
    # disability should be 3-2-1+1-1 = 0
    # auto should be 3-2-1+1=1
    # home should be 3-2-1=0
    # life should be 3-2-1+1+1 = 2

    result = calculate_risk_profile(user=user)
    assert result.disability == InsurancePlan.ECONOMIC
    assert result.auto == InsurancePlan.REGULAR
    assert result.home == InsurancePlan.ECONOMIC
    assert result.life == InsurancePlan.REGULAR
    assert result.renters is None
    assert result.umbrella == InsurancePlan.ECONOMIC


def test_risk_algorithm_house_rented():
    user = User(
        age=29,
        dependents=2,
        income=300000,
        marital_status=MaritalStatus.MARRIED,
        risk_questions=[True, True, True],
        house=House(ownership_status=HouseOwnershipStatus.RENTED),
        vehicle=Vehicle(year=int(time.strftime("%Y"))),
    )
    result = calculate_risk_profile(user=user)
    assert result.disability == InsurancePlan.ECONOMIC
    assert result.auto == InsurancePlan.REGULAR
    assert result.home is None
    assert result.renters == InsurancePlan.ECONOMIC
    assert result.life == InsurancePlan.REGULAR
    assert result.umbrella == InsurancePlan.ECONOMIC
