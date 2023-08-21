"""
API 관련 유틸 함수
"""

import base64


def is_audio_content_valid(
    audio_content: str,
) -> bool:
    """
    주어진 음성 데이터가 유효한지 검증한다.

    Args:
        audio_content (str): base64로 변환된 음성 데이터

    Returns:
        bool: 음성 데이터가 유효하면 True, 그렇지 않으면 False
    """

    try:
        decoded_audio = base64.b64decode(audio_content)

        if decoded_audio[:4] == b"RIFF":
            return True
        return False
    except (
        base64.binascii.Error,
        IndexError,
    ):
        return False
