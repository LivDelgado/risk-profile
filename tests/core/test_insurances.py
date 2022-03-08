from app.core.insurances import *
from app.models.user import *


def test_determine_final_profile_economic():
    score = -1
    result = Insurance.determine_final_profile(score)
    assert result == InsurancePlan.ECONOMIC

    score = 0
    result = Insurance.determine_final_profile(score)
    assert result == InsurancePlan.ECONOMIC


def test_determine_final_profile_regular():
    score = 1
    result = Insurance.determine_final_profile(score)
    assert result == InsurancePlan.REGULAR

    score = 2
    result = Insurance.determine_final_profile(score)
    assert result == InsurancePlan.REGULAR


def test_determine_final_profile_responsible():
    score = 3
    result = Insurance.determine_final_profile(score)
    assert result == InsurancePlan.RESPONSIBLE


def test_disability_insurance_line_ineligible_no_income():
    user = User(
        age=20,
        dependents=2,
        income=0,
        marital_status=MaritalStatus.MARRIED,
        risk_questions=[True, False, False],
    )
    base_score = 1

    result = Disability(user, base_score).get_insurance_plan_recommendation()
    assert result == InsurancePlan.INELIGIBLE


def test_disability_insurance_line_ineligible_older_than_60():
    user = User(
        age=61,
        dependents=2,
        income=1,
        marital_status=MaritalStatus.MARRIED,
        risk_questions=[True, False, False],
    )
    base_score = 1

    result = Disability(user, base_score).get_insurance_plan_recommendation()
    assert result == InsurancePlan.INELIGIBLE


def test_disability_insurance_line_eligible_with_all_rules():
    user = User(
        age=20,
        dependents=2,
        income=201000,
        marital_status=MaritalStatus.MARRIED,
        risk_questions=[True, True, True],
        house=House(ownership_status=HouseOwnershipStatus.OWNED),
    )
    base_score = 3

    # less than 30y -> -2
    # income > 200k -> -1
    # has dependents -> +1
    # is married -> -1

    # should become 0
    result = Disability(user, base_score).get_insurance_plan_recommendation()
    assert result == InsurancePlan.ECONOMIC


def test_auto_insurance_line_ineligible_no_vehicle():
    user = User(
        age=61,
        dependents=2,
        income=1,
        marital_status=MaritalStatus.MARRIED,
        risk_questions=[True, False, False],
    )
    base_score = 1

    result = Auto(user, base_score).get_insurance_plan_recommendation()
    assert result == InsurancePlan.INELIGIBLE


def test_auto_insurance_line():
    user = User(
        age=20,
        dependents=2,
        income=201,
        marital_status=MaritalStatus.MARRIED,
        risk_questions=[True, True, True],
        vehicle=Vehicle(year=int(time.strftime("%Y"))),
    )
    base_score = 3

    # should become 1
    result = Auto(user, base_score).get_insurance_plan_recommendation()
    assert result == InsurancePlan.REGULAR


def test_home_insurance_line_ineligible_no_house():
    user = User(
        age=61,
        dependents=2,
        income=1,
        marital_status=MaritalStatus.MARRIED,
        risk_questions=[True, False, False],
    )
    base_score = 1

    result = Home(user, base_score).get_insurance_plan_recommendation()
    assert result == InsurancePlan.INELIGIBLE


def test_home_insurance_line_eligible():
    user = User(
        age=20,
        dependents=2,
        income=201000,
        marital_status=MaritalStatus.MARRIED,
        risk_questions=[True, True, True],
        vehicle=Vehicle(year=int(time.strftime("%Y"))),
        house=House(ownership_status=HouseOwnershipStatus.OWNED),
    )
    base_score = 3

    # should become 0
    result = Home(user, base_score).get_insurance_plan_recommendation()
    assert result == InsurancePlan.ECONOMIC


def test_life_insurance_line_ineligible_older_than_60():
    user = User(
        age=61,
        dependents=2,
        income=1,
        marital_status=MaritalStatus.MARRIED,
        risk_questions=[True, False, False],
    )
    base_score = 1

    result = Life(user, base_score).get_insurance_plan_recommendation()
    assert result == InsurancePlan.INELIGIBLE


def test_life_insurance_line():
    user = User(
        age=20,
        dependents=2,
        income=201,
        marital_status=MaritalStatus.MARRIED,
        risk_questions=[True, True, True],
        vehicle=Vehicle(year=int(time.strftime("%Y"))),
        house=House(ownership_status=HouseOwnershipStatus.OWNED),
    )
    base_score = 2

    # should become 1
    result = Life(user, base_score).get_insurance_plan_recommendation()
    assert result == InsurancePlan.REGULAR


def test_umbrella_insurance_line_economic_main_line():
    main_line_plans = [InsurancePlan.INELIGIBLE, InsurancePlan.ECONOMIC]
    user = User(
        age=20,
        dependents=2,
        income=50000,
        marital_status=MaritalStatus.MARRIED,
        risk_questions=[True, True, True],
        vehicle=Vehicle(year=int(time.strftime("%Y"))),
        house=House(ownership_status=HouseOwnershipStatus.OWNED),
    )
    base_score = 3

    result = Umbrella(
        user, base_score, main_line_plans
    ).get_insurance_plan_recommendation()
    assert result == InsurancePlan.REGULAR


def test_umbrella_insurance_line_no_economic_main_line():
    main_line_plans = [InsurancePlan.INELIGIBLE, InsurancePlan.REGULAR]
    user = User(
        age=20,
        dependents=2,
        income=50000,
        marital_status=MaritalStatus.MARRIED,
        risk_questions=[True, True, True],
        vehicle=Vehicle(year=int(time.strftime("%Y"))),
        house=House(ownership_status=HouseOwnershipStatus.OWNED),
    )
    base_score = 3

    result = Umbrella(
        user, base_score, main_line_plans
    ).get_insurance_plan_recommendation()
    assert result == InsurancePlan.INELIGIBLE
