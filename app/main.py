from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from gunicorn.http import Request
from starlette import status
from starlette.responses import JSONResponse

from .routers import risk_profiles

title = "Insurance Plan Recommendation"
description = "Service responsible by managing insurance plan recommendations based on risk profile analysis"

app = FastAPI(
    title=title,
    description=description,
    version="0.1.0",
    contact={
        "name": "Lívia",
        "url": "https://github.com/livdelgado",
        "email": "liviadelgado.dev@gmail.com",
    },
    docs_url="/",
    redoc_url="/docs"
)

app.include_router(risk_profiles.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


