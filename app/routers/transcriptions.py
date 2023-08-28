"""
음성 인식 관련 엔드포인트
"""

import base64
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from google.cloud import speech_v2
from google.api_core.exceptions import GoogleAPIError

from app.api.models import TranscriptionCreate, TranscriptionResponse
from app.core.exceptions import CustomException
from app.api.utils import is_audio_content_valid

from app.core.config import speech_recognition_config
from app.settings.constants import *

router = APIRouter(prefix=f"/api/{STT_API_VERSION_LATEST}")

client = speech_v2.SpeechClient.from_service_account_file("app/settings/key.json")


@router.post(
    "/transcriptions",
    response_model=TranscriptionResponse,
    description="음성 인식 API",
    tags=["transcriptions"],
)
async def create_transcription(audio: TranscriptionCreate) -> JSONResponse:
    """
    음성 데이터를 인식한 결과(텍스트)를 반환한다.

    Args:
        audio (TranscriptionCreate): 음성 인식을 하려는 파일을 base64로 인코딩 한 값

    Returns:
        JSONResponse: 음성 인식 결과
    """

    try:
        if not is_audio_content_valid(audio.audio):
            raise CustomException(
                status_code=HTTP_STATUS_CODE["BAD_REQUEST"],
                message=HTTP_STATUS_MESSAGE["BAD_REQUEST"],
                attribute="audio",
                reason="The audio data provided is not supported. Please send a valid audio.",
            )

        decoded_audio = base64.b64decode(audio.audio)

        request = speech_v2.RecognizeRequest(
            recognizer=f"projects/{GCP_PROJECT_ID}/locations/global/recognizers/_",
            content=decoded_audio,
            config=speech_recognition_config,
        )

        response = client.recognize(request=request)

        if not response.results:
            raise CustomException(
                status_code=HTTP_STATUS_CODE["BAD_REQUEST"],
                message=HTTP_STATUS_MESSAGE["BAD_REQUEST"],
                attribute="audio",
                reason="The audio quality might be low. Please provide clearer audio.",
            )

        result = response.results[0].alternatives[0]

        [transcript, confidence] = [result.transcript, result.confidence]

        if confidence < STT_API_CONFIDENCE_THRESHOLD:
            raise CustomException(
                status_code=HTTP_STATUS_CODE["BAD_REQUEST"],
                message=HTTP_STATUS_MESSAGE["BAD_REQUEST"],
                attribute="audio",
                reason="The audio quality might be low. Please provide clearer audio.",
            )

        return JSONResponse(
            status_code=HTTP_STATUS_CODE["OK"],
            content={
                "status": "success",
                "code": HTTP_STATUS_CODE["OK"],
                "message": HTTP_STATUS_MESSAGE["OK"],
                "data": {"transcription": transcript},
            },
        )

    except (CustomException, Exception) as exc:
        if isinstance(exc, CustomException):
            raise exc
        if isinstance(exc, GoogleAPIError):
            raise CustomException(
                status_code=HTTP_STATUS_CODE["INTERNAL_SERVER_ERROR"],
                message=HTTP_STATUS_MESSAGE["INTERNAL_SERVER_ERROR"],
                attribute="external",
                reason="An error occurred while communicating with other servers. Please try again later.",
            ) from exc
        raise CustomException(
            status_code=HTTP_STATUS_CODE["INTERNAL_SERVER_ERROR"],
            message=HTTP_STATUS_MESSAGE["INTERNAL_SERVER_ERROR"],
            attribute="internal",
            reason="An error occurred while processing the request. Please try again later.",
        ) from exc
