"""
app.core.exception_handlers 모듈의 함수들에 대한 테스트
"""

import json
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import CustomException
from app.core.exception_handlers import create_error_response, custom_exception_handler
from app.settings.constants import HTTP_STATUS_CODE, HTTP_STATUS_MESSAGE


def convert_json_response_to_dict(response):
    """JSONResponse를 딕셔너리 형태로 변환하는 함수"""

    response_content_bytes = response.body
    response_content_str = response_content_bytes.decode("utf-8")

    return json.loads(response_content_str)


def test_create_error_response():
    """create_error_response 함수에 대한 테스트"""

    # Arrange
    status_code = HTTP_STATUS_CODE["BAD_REQUEST"]
    message = HTTP_STATUS_MESSAGE["BAD_REQUEST"]
    attribute = "attribute_name"
    reason = "Invalid value"

    # Act
    response = create_error_response(status_code, message, attribute, reason)

    # Assert
    assert response.status_code == HTTP_STATUS_CODE["BAD_REQUEST"]
    assert convert_json_response_to_dict(response) == {
        "status": "error",
        "code": status_code,
        "message": message,
        "details": {"attribute": attribute, "reason": reason},
    }


def test_custom_exception_handler_custom_error():
    """custom_exception_handler 함수에 대한 테스트: CustomException 발생 케이스"""

    # Arrange
    exception = CustomException(
        status_code=HTTP_STATUS_CODE["BAD_REQUEST"],
        message=HTTP_STATUS_MESSAGE["BAD_REQUEST"],
        attribute="attribute_name",
        reason="Invalid value",
    )

    # Act
    response = custom_exception_handler("", exception)

    # Assert
    assert response.status_code == HTTP_STATUS_CODE["BAD_REQUEST"]
    assert convert_json_response_to_dict(response) == {
        "status": "error",
        "code": HTTP_STATUS_CODE["BAD_REQUEST"],
        "message": HTTP_STATUS_MESSAGE["BAD_REQUEST"],
        "details": {"attribute": "attribute_name", "reason": "Invalid value"},
    }


def test_custom_exception_handler_request_validation_error_missing_required_field():
    """
    custom_exception_handler 함수에 대한 테스트:
    RequestValidationError 발생 케이스 (필수 필드가 비어 있는 경우)
    """

    # Arrange
    errors = [
        {
            "loc": ["body", "field"],
            "input": "field",
            "msg": "field required",
            "type": "missing",
        }
    ]
    exception = RequestValidationError(errors)

    # Act
    response = custom_exception_handler("", exception)

    # Assert
    assert response.status_code == HTTP_STATUS_CODE["BAD_REQUEST"]
    assert convert_json_response_to_dict(response) == {
        "status": "error",
        "code": HTTP_STATUS_CODE["BAD_REQUEST"],
        "message": HTTP_STATUS_MESSAGE["BAD_REQUEST"],
        "details": {
            "attribute": "field",
            "reason": "The required field `field` is missing. Please check your request.",
        },
    }


def test_custom_exception_handler_request_validation_error_missing_body():
    """
    custom_exception_handler 함수에 대한 테스트:
    RequestValidationError 발생 케이스 (body가 비어 있는 경우)
    """

    # Arrange
    errors = [
        {
            "loc": ["body", "field"],
            "msg": "field required",
            "input": None,
            "type": "missing",
        }
    ]
    exception = RequestValidationError(errors)

    # Act
    response = custom_exception_handler("", exception)

    # Assert
    assert response.status_code == HTTP_STATUS_CODE["BAD_REQUEST"]
    assert convert_json_response_to_dict(response) == {
        "status": "error",
        "code": HTTP_STATUS_CODE["BAD_REQUEST"],
        "message": HTTP_STATUS_MESSAGE["BAD_REQUEST"],
        "details": {
            "attribute": "",
            "reason": "The request body is empty. Please check your request.",
        },
    }


def test_custom_exception_handler_request_validation_error_wrong_field_type():
    """
    custom_exception_handler 함수에 대한 테스트:
    RequestValidationError 발생 케이스 (필드 타입이 문자형이 아닌 경우)
    """

    # Arrange
    errors = [
        {
            "loc": ["body", "field"],
            "msg": "field required",
            "input": None,
            "type": "string_type",
        }
    ]
    exception = RequestValidationError(errors)

    # Act
    response = custom_exception_handler("", exception)

    # Assert
    assert response.status_code == HTTP_STATUS_CODE["BAD_REQUEST"]
    assert convert_json_response_to_dict(response) == {
        "status": "error",
        "code": HTTP_STATUS_CODE["BAD_REQUEST"],
        "message": HTTP_STATUS_MESSAGE["BAD_REQUEST"],
        "details": {
            "attribute": "field",
            "reason": "The field `field` should be string type.",
        },
    }


def test_custom_exception_handler_request_the_other_error():
    """
    custom_exception_handler 함수에 대한 테스트:
    CustomException, RequestValidation 이외의 케이스
    """

    # Arrange
    exception = Exception("The other error")

    # Act
    response = custom_exception_handler("", exception)

    # Assert
    assert response.status_code == HTTP_STATUS_CODE["INTERNAL_SERVER_ERROR"]
    assert convert_json_response_to_dict(response) == {
        "status": "error",
        "code": HTTP_STATUS_CODE["INTERNAL_SERVER_ERROR"],
        "message": HTTP_STATUS_MESSAGE["INTERNAL_SERVER_ERROR"],
        "details": {
            "attribute": "internal",
            "reason": "An internal error occurred while processing the request. Please try again later.",
        },
    }
