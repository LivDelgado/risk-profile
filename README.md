# Risk Profile App

## Description

Determine user insurance needs based on risk profile.

Developed with FastAPI, Python 3.10.2.

## Project links
This project is deployed to [Heroku](https://www.heroku.com/).

- [Swagger Docs](https://risk-profile.herokuapp.com/)
- [OpenAPI Docs](https://risk-profile.herokuapp.com/docs)


## How to run the code locally

This project runs on Python 3.10.2, so you should have this version
installed.
[Python Release link](https://www.python.org/downloads/release/python-3102/).


The installation should come with `pip`.

Then, you need to install the project dependencies.
They can be found in the requirements file.

```bash
pip install -r requirements.txt
```

The final step is to run the local server. In the console it will show
the correct port, but it should be found at [http://localhost:8000](http://127.0.0.1:8000).

```bash
uvicorn app.main:app --reload
```

### Running the tests

```bash
pytest
```

## About the code decisions / Problem Understanding

### Testing

Tests implemented using pytest.
Unit tests and TestClient (FastAPI) tests.

### Risk calculation - Rules

This table was created based on the rules described in 
the assignment for better understanding 

| Rule | Disability | Auto | Home | Life |
| --- | --- | --- | --- | --- |
| No income | Ineligible |  |  |  |
| No vehicle |  | Ineligible |  |  |
| No house |  |  | Ineligible |  |
| >60yo | Ineligible |  |  | Ineligible |
| <30yo | -2 | -2 | -2 | -2 |
| 30y≤x≤40y | -1 | -1 | -1 | -1 |
| Income >200k | -1 | -1 | -1 | -1 |
| House is mortgaged | +1 |  | +1 |  |
| Has dependents | +1 |  |  | +1 |
| Married | -1 |  |  | +1 |
| Vehicle produced in the last 5y |  | +1 |  |  |

### Plan Recommendation

| ≤0 | Economic |
| --- | --- |
| 1 or 2 | Regular |
| ≥ 3 | Responsible |

### Architecture

The core of the application is to determine the risk profile 
for each line of insurance.

The design was created from the [Rules Design Pattern](https://levelup.gitconnected.com/rules-design-pattern-in-c-6c62f0e20ee0).

In the `app.core.insurances` file, I have defined all the insurance lines
with the rules list.

These classes have a method to verify and apply all these rules, updating the risk score 
if needed.

To add a new insurance line, we need to create a new class that inherits from
the `Insurance` class and define the rules list - besides adding it to the model property and 
in the `calculate_risk_profile` method to be returned as a model field.

The `Rule` classes have two main methods: `should_apply` and `apply`,
which verify if the User matches the rule and apply the rule, updating the risk score
or defining the final risk profile for the insurance line.

Each rule is independent, and we can add more rules that inherit from one of the main
classes (`Rule`, `AddToRiskScore`, `DeductFromRiskScore`, `Ineligible`).

The application flow can be described as following:
1. Receive POST request
2. Validate request
3. Calculate base score based on risk questions
4. For each insurance line, apply rules and get the 
final score, then convert it to a risk profile
 