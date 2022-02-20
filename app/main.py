from fastapi import FastAPI
from .routers import insurances

app = FastAPI()

app.include_router(insurances.router)
