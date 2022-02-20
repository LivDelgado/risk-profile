from enum import Enum
from typing import List
from pydantic import BaseModel, validator
import time

RiskAnswers = List[bool]


class MarritalStatus(Enum):
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
        current_year = time.strftime("%Y")
        if not (first_car_year <= v <= current_year):
            raise ValueError(f'invalid year {v}')


class User(BaseModel):
    age: int
    dependents: int
    income: int
    marital_status: MarritalStatus
    risk_answers: RiskAnswers
    house: House | None = None
    vehicle: Vehicle | None = None

    class Config:
        arbitrary_types_allowed = True

    @validator('age', 'dependents', 'income')
    def gte_zero_validator(cls, v):
        if v < 0:
            raise ValueError(f'{v} should be greater than or equal to zero')
        return v

    @validator('risk_answers')
    def risk_answers_validator(cls, v):
        print(v)
        if len(v) != 3:
            raise ValueError(f'{v} should have 3 elements')
        return v
