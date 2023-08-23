"""
어플리케이션의 메인 모듈
"""

from fastapi import FastAPI

from fastapi.exceptions import RequestValidationError
from app.core.exceptions import CustomException
from app.core.exception_handlers import custom_exception_handler

from app.routers import transcriptions, predictions

app = FastAPI()

app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, custom_exception_handler)

app.include_router(transcriptions.router)
app.include_router(predictions.router)
