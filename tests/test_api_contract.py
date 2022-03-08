import time
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


valid_request = {
    "age": 35,
    "dependents": 2,
    "house": {"ownership_status": "owned"},
    "income": 0,
    "marital_status": "married",
    "risk_questions": [0, 1, 0],
    "vehicle": {"year": 2018},
}


def test_valid_request():
    response = client.post(
        "/risk-profiles/",
        json=valid_request,
    )
    assert response.status_code == 200
    assert response.json() == {
        "auto": "regular",
        "disability": "ineligible",
        "home": "economic",
        "life": "regular",
    }


def test_ineligibility_low_income_high_risk():
    request = {
        "age": 35,
        "dependents": 2,
        "house": {"ownership_status": "owned"},
        "income": 20000,
        "marital_status": "married",
        "risk_questions": [0, 0, 0],
        "vehicle": {"year": 2018},
    }

    response = client.post(
        "/risk-profiles/",
        json=request,
    )
    assert response.status_code == 200
    assert response.json() == {
        "auto": "ineligible",
        "disability": "ineligible",
        "home": "ineligible",
        "life": "ineligible",
    }


def test_valid_request_no_house_nor_vehicle():
    request = valid_request
    request.pop("house")
    request.pop("vehicle")
    response = client.post(
        "/risk-profiles/",
        json=request,
    )
    assert response.status_code == 200
    assert response.json() == {
        "auto": "ineligible",
        "disability": "ineligible",
        "home": "ineligible",
        "life": "regular",
    }


def test_invalid_age():
    response = client.post(
        "/risk-profiles/",
        json={
            "age": -1,
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 0,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018},
        },
    )
    assert response.status_code == 400


def test_invalid_dependents():
    response = client.post(
        "/risk-profiles/",
        json={
            "age": 18,
            "dependents": -3,
            "house": {"ownership_status": "owned"},
            "income": 0,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018},
        },
    )
    assert response.status_code == 400


def test_invalid_income():
    response = client.post(
        "/risk-profiles/",
        json={
            "age": 18,
            "dependents": 0,
            "house": {"ownership_status": "owned"},
            "income": -1,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018},
        },
    )
    assert response.status_code == 400


def test_invalid_marital_status():
    response = client.post(
        "/risk-profiles/",
        json={
            "age": 18,
            "dependents": 0,
            "house": {"ownership_status": "owned"},
            "income": 1,
            "marital_status": "playing_around",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018},
        },
    )
    assert response.status_code == 400


def test_invalid_risk_answers():
    response = client.post(
        "/risk-profiles/",
        json={
            "age": 18,
            "dependents": 0,
            "house": {"ownership_status": "owned"},
            "income": 1,
            "marital_status": "single",
            "risk_questions": [0, 1],
            "vehicle": {"year": 2018},
        },
    )
    assert response.status_code == 400


def test_invalid_house_ownership_status():
    response = client.post(
        "/risk-profiles/",
        json={
            "age": 18,
            "dependents": 0,
            "house": {"ownership_status": "rent"},
            "income": 1,
            "marital_status": "single",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018},
        },
    )
    assert response.status_code == 400


def test_invalid_car_year():
    response = client.post(
        "/risk-profiles/",
        json={
            "age": 18,
            "dependents": 0,
            "house": {"ownership_status": "rent"},
            "income": 1,
            "marital_status": "single",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 1885},
        },
    )
    assert response.status_code == 400

    response = client.post(
        "/risk-profiles/",
        json={
            "age": 18,
            "dependents": 0,
            "house": {"ownership_status": "rent"},
            "income": 1,
            "marital_status": "single",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": int(time.strftime("%Y")) + 1},
        },
    )
    assert response.status_code == 400
