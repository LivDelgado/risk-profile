from enum import Enum
from typing import List
from pydantic import BaseModel, validator
import time

RiskAnswers = List[bool]


class MaritalStatus(Enum):
    SINGLE = "single"
    MARRIED = "married"


class HouseOwnershipStatus(Enum):
    OWNED = "owned"
    MORTGAGED = "mortgaged"


class House(BaseModel):
    ownership_status: HouseOwnershipStatus


class Vehicle(BaseModel):
    year: int

    @validator('year')
    def year_validator(cls, v):
        first_car_year = 1886
        current_year = int(time.strftime("%Y"))
        if not (first_car_year <= v <= current_year):
            raise ValueError(f'invalid year {v}')

        return v


class User(BaseModel):
    age: int
    dependents: int
    income: int
    marital_status: MaritalStatus
    risk_questions: RiskAnswers
    house: House | None = None
    vehicle: Vehicle | None = None

    class Config:
        arbitrary_types_allowed = True

    @validator('age', 'dependents', 'income')
    def gte_zero_validator(cls, v):
        if v < 0:
            raise ValueError(f'{v} should be greater than or equal to zero')
        return v

    @validator('risk_questions')
    def risk_questions_validator(cls, v):
        if len(v) != 3:
            raise ValueError(f'{v} should have 3 elements')
        return v
