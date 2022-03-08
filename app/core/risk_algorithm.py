from typing import List
from app.models.user import User
from app.models.risk_profile import InsurancePlanRecommendation
from .insurances import Disability, Auto, Home, Life, Renters, Umbrella


def calculate_base_score(risk_questions: List[bool]) -> int:
    """
    Calculates the base score based on the risk questions results

    :param risk_questions: list of boolean with user's answers
    :return: integer with final base score value
    """
    return sum(risk_questions)


def calculate_risk_profile(user: User) -> InsurancePlanRecommendation:
    """
    Determines the risk profile for each line of insurance and then suggests an insurance plan
    ("economic", "regular", "responsible") corresponding to the risk profile

    :param user: User whose risk profile will be analysed
    :return: Insurance Plan Recommendation
    """
    base_score = calculate_base_score(user.risk_questions)

    disability = Disability(user, base_score).recommend_plan_when_applicable()
    auto = Auto(user, base_score).recommend_plan_when_applicable()
    home = Home(user, base_score).recommend_plan_when_applicable()
    life = Life(user, base_score).recommend_plan_when_applicable()
    renters = Renters(user, base_score).recommend_plan_when_applicable()

    main_insurance_plans = [life, disability, home, auto]

    umbrella = Umbrella(
        user, base_score, main_insurance_plans
    ).recommend_plan_when_applicable()

    return InsurancePlanRecommendation(
        auto=auto,
        disability=disability,
        home=home,
        life=life,
        renters=renters,
        umbrella=umbrella,
    )
