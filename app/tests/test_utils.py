"""
app.api.utils 모듈의 유틸 함수들에 대한 테스트
"""

import base64
import pytest
from app.api.utils import is_audio_content_valid


@pytest.mark.parametrize(
    "audio_content, expected",
    [
        ("not_base64", False),
        (base64.b64encode(b"INVALID" + b"random bytes").decode("utf-8"), False),
        (base64.b64encode(b"RIFF" + b"random bytes").decode("utf-8"), True),
    ],
)
def test_is_audio_content_valid(audio_content, expected):
    """is_audio_content_valid 함수에 대한 테스트"""

    assert is_audio_content_valid(audio_content) == expected
