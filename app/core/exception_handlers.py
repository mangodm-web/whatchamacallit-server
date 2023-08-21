"""
예외처리와 에러 응답을 생성하는 모듈
"""

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import CustomException
from app.settings.constants import HTTP_STATUS_CODE, HTTP_STATUS_MESSAGE


def create_error_response(
    status_code: int, message: str, attribute: str, reason: str
) -> JSONResponse:
    """
    규격화된 JSON 에러 응답을 생성한다.

    Args:
        status_code (int): HTTP 응답 상태코드
        message (str): HTTP 관련 메시지
        attribute (str): 에러와 관련된 속성
        reason (str): 에러 발생 사유

    Returns:
        JSONResponse: 에러 정보를 담고 있는 JSON 응답 객체
    """

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "code": status_code,
            "message": message,
            "details": {"attribute": attribute, "reason": reason},
        },
    )


def custom_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    예외 케이스가 발생했을 경우, 규격화된 에러를 반환할 수 있도록 처리한다.

    Args:
        _ (Request): FastAPI Request 객체
        exc (Exception): 처리할 Exception 인스턴스

    Returns:
        JSONResponse: 규격화된 에러 정보를 담고 있는 JSON 응답 객체
    """

    if isinstance(exc, CustomException):
        return create_error_response(
            exc.status_code, exc.message, exc.attribute, exc.reason
        )

    if isinstance(exc, RequestValidationError):
        field = ""
        message = ""

        for error in exc.errors():
            if error["type"] == "missing":
                input_field = error["input"]

                if input_field is not None:
                    field += error["loc"][1]
                    message += f"The required field `{field}` is missing. Please check your request."
                else:
                    field += ""
                    message += "The request body is empty. Please check your request."
            if error["type"] == "string_type":
                field += error["loc"][1]
                message += f"The field `{field}` should be string type."

        return create_error_response(
            HTTP_STATUS_CODE["BAD_REQUEST"],
            HTTP_STATUS_MESSAGE["BAD_REQUEST"],
            field,
            message,
        )

    return create_error_response(
        HTTP_STATUS_CODE["INTERNAL_SERVER_ERROR"],
        HTTP_STATUS_MESSAGE["INTERNAL_SERVER_ERROR"],
        "internal",
        "An internal error occurred while processing the request. Please try again later.",
    )
