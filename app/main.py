"""
어플리케이션의 메인 모듈
"""

import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions import CustomException
from app.core.exception_handlers import custom_exception_handler

from app import global_config
from app.routers import transcriptions, predictions

from app.settings.constants import ALLOWED_ORIGINS

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Authorization", "Content-Type"],
)

app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, custom_exception_handler)

app.include_router(transcriptions.router)
app.include_router(predictions.router)
