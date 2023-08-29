"""
단어 추론 관련 엔드포인트
"""

from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.models import (
    PredictionCreate,
    PredictionResponse,
    FeedbackCreate,
    FeedbackResponse,
)
from app.core.exceptions import CustomException
from app.settings.constants import (
    HTTP_STATUS_CODE,
    HTTP_STATUS_MESSAGE,
    MODEL_API_VERSION_LATEST,
)

from app.core.mongodb_utils import get_mongodb_client, insert_document

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


@router.post(
    "/predictions/feedback",
    response_model=FeedbackResponse,
    summary="단어 추론 결과에 대한 피드백 API",
    description="추론 결과에 대한 사용자의 피드백을 처리한다.",
    tags=["predictions", "feedback"],
)
async def create_feedback(feedback: FeedbackCreate) -> JSONResponse:
    """
    단어 추론 결과에 대한 사용자의 피드백을 처리한다.

    Args:
        feedback (FeedbackCreate): 사용자가 제공한 피드백

    Returns:
        JSONResponse: 피드백 처리 결과
    """

    if not feedback:
        raise CustomException(
            status_code=HTTP_STATUS_CODE["BAD_REQUEST"],
            message=HTTP_STATUS_MESSAGE["BAD_REQUEST"],
            attribute="feedback",
            reason="The provided feedback is not in the correct format. Please resend the data.",
        )

    try:
        mongodb_client = get_mongodb_client()
    except Exception as exc:
        raise CustomException(
            status_code=HTTP_STATUS_CODE["INTERNAL_SERVER_ERROR"],
            message=HTTP_STATUS_MESSAGE["INTERNAL_SERVER_ERROR"],
            attribute="mongodb",
            reason="An internal error occurred while connecting to MongoDB. Please try again later.",
        ) from exc

    try:
        created_id = insert_document(
            mongodb_client,
            "feedback_data",
            {
                "description": feedback.description,
                "user_input": feedback.user_input,
                "predictions": feedback.predictions,
                "version_model": feedback.version_model,
                "created_date": datetime.now(),
                "correct_prediction_index": feedback.correct_prediction_index,
            },
        )

        return JSONResponse(
            status_code=HTTP_STATUS_CODE["CREATED"],
            content={
                "status": "success",
                "code": HTTP_STATUS_CODE["CREATED"],
                "message": HTTP_STATUS_MESSAGE["CREATED"],
                "data": {"_id": created_id},
            },
        )
    except CustomException as exc:
        raise exc
    except Exception as exc:
        raise CustomException(
            status_code=HTTP_STATUS_CODE["INTERNAL_SERVER_ERROR"],
            message=HTTP_STATUS_MESSAGE["INTERNAL_SERVER_ERROR"],
            attribute="general",
            reason="An internal error occurred while processing your feeback. Please try again later.",
        ) from exc
    finally:
        mongodb_client.close()
