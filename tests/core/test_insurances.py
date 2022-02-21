from app.core.insurances import *


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
