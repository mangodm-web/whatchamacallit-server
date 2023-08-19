from fastapi import HTTPException


class CustomException(HTTPException):
    def __init__(self, status_code: int, message: str, attribute: str, reason: str):
        """
        CustomException 인스턴스를 초기화한다.

        Args:
            status_code (int): 에러의 HTTP 상태 코드
            message (str): 에러 메시지
            attribute (str): 에러와 관련된 속성 값(혹은 필드명)
            reason (str): 에러가 발생한 이유에 대한 정보

        Returns:
            CustomException: CustomException 인스턴스
        """

        self.status_code = status_code
        self.message = message
        self.attribute = attribute
        self.reason = reason
        super().__init__(status_code=status_code, detail=message)
