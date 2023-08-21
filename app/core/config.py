"""
음성 인식 API와 관련된 설정을 위한 모듈
"""

from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech

speech_recognition_config = speech_v2.RecognitionConfig(
    auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
    language_codes=["en-US"],
    model="short",
)
