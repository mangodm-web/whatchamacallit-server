from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import CustomException


def custom_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
    """
    CustomException 인스턴스를 규격화된 에러 응답으로 변환한다.

    Args:
        request (Request): FastAPI Request 객체
        exc (CustomException): 처리할 CustomException 인스턴스

    Returns:
        JSONResponse: 규격화된 에러 정보를 담고 있는 JSON 응답 객체
    """

    error_response = {
        "status": "error",
        "code": exc.status_code,
        "message": exc.message,
        "details": {
            "attribute": exc.attribute,
            "reason": exc.reason,
        },
    }

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response,
    )
