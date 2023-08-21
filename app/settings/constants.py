"""
상수(constants) 변수 모음
"""

import os
from dotenv import load_dotenv

from fastapi import status

load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")

MODEL_API_VERSION_LATEST = "v1"
STT_API_VERSION_LATEST = "v1"
STT_API_CONFIDENCE_THRESHOLD = 0.5

HTTP_STATUS_CODE = {
    "OK": status.HTTP_200_OK,
    "BAD_REQUEST": status.HTTP_400_BAD_REQUEST,
    "INTERNAL_SERVER_ERROR": status.HTTP_500_INTERNAL_SERVER_ERROR,
}
HTTP_STATUS_MESSAGE = {
    "OK": "OK",
    "BAD_REQUEST": "Bad Request",
    "INTERNAL_SERVER_ERROR": "Internal Server Error",
}
