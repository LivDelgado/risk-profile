from enum import Enum
from typing import List

class MarritalStatus(Enum):
    SINGLE = "single"
    MARRIED = "married"

class User:
    age : int
    dependents : int
    income : int
    marital_status : MarritalStatus
    risk_answers : List[bool]