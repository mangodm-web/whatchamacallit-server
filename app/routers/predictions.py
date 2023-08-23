"""
단어 추론 관련 엔드포인트
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.models import PredictionCreate, PredictionResponse
from app.core.exceptions import CustomException
from app.settings.constants import (
    HTTP_STATUS_CODE,
    HTTP_STATUS_MESSAGE,
    MODEL_API_VERSION_LATEST,
)

from app.services.model_inference import get_predictions

router = APIRouter(prefix=f"/api/{MODEL_API_VERSION_LATEST}")


@router.post(
    "/predictions",
    response_model=PredictionResponse,
    summary="단어 추론 API",
    description="사용자의 설명에 가장 가까운 단어를 반환한다.",
    tags=["predictions"],
)
async def create_prediction(description: PredictionCreate) -> JSONResponse:
    """
    단어 추론 결과를 반환한다.

    Args:
        description (PredictionCreate): 단어에 대한 설명

    Returns:
        JSONResponse: 단어 추론 결과
    """

    query = description.description

    if not query or query.strip() == "":
        raise CustomException(
            status_code=HTTP_STATUS_CODE["BAD_REQUEST"],
            message=HTTP_STATUS_MESSAGE["BAD_REQUEST"],
            attribute="description",
            reason="The description is empty. Please check the data and resend it.",
        )

    try:
        predictions = get_predictions(query)

        return JSONResponse(
            status_code=HTTP_STATUS_CODE["OK"],
            content={
                "status": "success",
                "code": HTTP_STATUS_CODE["OK"],
                "message": HTTP_STATUS_MESSAGE["OK"],
                "data": {"predictions": predictions},
            },
        )
    except CustomException as exc:
        raise exc
    except Exception as exc:
        raise CustomException(
            status_code=HTTP_STATUS_CODE["INTERNAL_SERVER_ERROR"],
            message=HTTP_STATUS_MESSAGE["INTERNAL_SERVER_ERROR"],
            attribute="model",
            reason="An error occurred while performing model inference. Please try again later.",
        ) from exc
