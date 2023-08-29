"""
API 관련 요청, 응답 스키마 정의
"""

from pydantic import BaseModel
from typing import List


class TranscriptionCreate(BaseModel):
    """
    음성 인식 API 요청 시 전송해야 하는 본문 데이터 구조

    Attributes:
        audio (str): 음성 인식을 하려는 파일을 base64로 인코딩 한 값
    """

    audio: str


class TranscriptionResponse(BaseModel):
    """
    음성 인식 결과를 담은 응답 데이터 구조

    Attributes:
        status (str): 응답 상태 ("success" 혹은 "error")
        code (int): HTTP 응답 상태코드
        message (str): HTTP 관련 메시지
        data (dict): 음성 인식 결과 데이터 (응답 상태가 성공인 경우에만 존재)
        details (dict): 에러 응답 세부 정보 (응답 상태가 실패인 경우에만 존재)
    """

    status: str
    code: int
    message: str
    data: dict = None
    details: dict = None


class PredictionCreate(BaseModel):
    """
    단어 추론 API 요청 시 전송해야 하는 본문 데이터 구조

    Attributes:
        description (str): 단어를 추론하는데 사용될 단어에 관한 묘사 텍스트
    """

    description: str


class PredictionResponse(BaseModel):
    """
    단어 추론 결과를 담은 응답 데이터 구조

    Attributes:
        status (str): 응답 상태 ("success" 혹은 "error")
        code (int): HTTP 응답 상태코드
        message (str): HTTP 관련 메시지
        data (dict): 단어 추론 결과 데이터 (응답 상태가 성공인 경우에만 존재)
        details (dict): 에러 응답 세부 정보 (응답 상태가 실패인 경우에만 존재)
    """

    status: str
    code: int
    message: str
    data: dict = None
    details: dict = None


class FeedbackCreate(BaseModel):
    """
    단어 추론에 대한 피드백 API 요청 시 전송해야 하는 본문 데이터 구조

    Attributes:
        description (str): 단어를 추론하는데 사용될 단어에 관한 묘사 텍스트
        user_input (str): 사용자가 입력한 답
        predictions (List): 모델이 예측한 답
        version_model (str): 추론 결과를 만든 모델 버전
        correct_prediction_index (int): 추론 결과의 인덱스 값, 예측 배열에 없을 시 -1
    """

    description: str
    user_input: str
    predictions: List
    version_model: str
    correct_prediction_index: int


class FeedbackResponse(BaseModel):
    """
    단어 추론에 대한 피드백 API 요청 시 전송하는 응답 데이터 구조

    Attributes:
        status (str): 응답 상태 ("success" 혹은 "error")
        code (int): HTTP 응답 상태코드
        message (str): HTTP 관련 메시지
        data (dict): 결과 데이터 (응답 상태가 성공인 경우에만 존재)
        details (dict): 에러 응답 세부 정보 (응답 상태가 실패인 경우에만 존재)
    """

    status: str
    code: int
    message: str
    data: dict = None
    details: dict = None
