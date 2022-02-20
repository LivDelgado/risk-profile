from typing import List
from app.models.user import User
from app.models.risk_profile import RiskProfile
from .insurances import Disability, Auto, Home, Life


def calculate_base_score(risk_questions: List[bool]):
    return sum(risk_questions)


def calculate_risk_score(user: User) -> RiskProfile:
    base_score = calculate_base_score(user.risk_questions)
    disability = Disability(user, base_score).determine_risk_score()
    auto = Auto(user, base_score).determine_risk_score()
    home = Home(user, base_score).determine_risk_score()
    life = Life(user, base_score).determine_risk_score()

    return RiskProfile(auto=auto, disability=disability, home=home, life=life)

