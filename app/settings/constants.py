"""
상수(constants) 변수 모음
"""

import os
from dotenv import load_dotenv
from fastapi import status

load_dotenv()

# Google Cloud Platform 관련
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")

# MongoDB 관련
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")

# AWS S3 관련
AWS_S3_BUCKET_NAME = os.getenv("WCC_AWS_S3_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("WCC_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("WCC_AWS_SECRET_ACCESS_KEY")

# 모델 관련
MODEL_API_VERSION_LATEST = "v1"
MODEL_S3_PATH = f"models/{MODEL_API_VERSION_LATEST}/model.zip"
MODEL_LOCAL = f"app/settings/model/{MODEL_API_VERSION_LATEST}"
MODEL_LOCAL_PATH = f"app/settings/model/{MODEL_API_VERSION_LATEST}/model.zip"

# 음성인식 / STT(Speech-to-Text) 관련
STT_API_VERSION_LATEST = "v1"
STT_API_CONFIDENCE_THRESHOLD = 0.5

# HTTP 상태 코드
HTTP_STATUS_CODE = {
    "OK": status.HTTP_200_OK,
    "BAD_REQUEST": status.HTTP_400_BAD_REQUEST,
    "INTERNAL_SERVER_ERROR": status.HTTP_500_INTERNAL_SERVER_ERROR,
}

# HTTP 상태 메시지
HTTP_STATUS_MESSAGE = {
    "OK": "OK",
    "BAD_REQUEST": "Bad Request",
    "INTERNAL_SERVER_ERROR": "Internal Server Error",
}
