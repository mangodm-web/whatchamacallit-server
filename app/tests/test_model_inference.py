"""
app.services.model_inference 모듈의 함수에 대한 테스트
"""

import pytest
from app.services.model_inference import get_predictions


# Arrange
@pytest.mark.parametrize(
    "query, expected",
    [
        ("", []),
        (
            "A place in New York where a lot of people are gathering.....",
            [
                {"text": "Times Square", "rank": 1},
                {"text": "Colosseum", "rank": 2},
                {"text": "Western Wall", "rank": 3},
            ],
        ),
    ],
)
def test_get_predictions(query, expected):
    """get_predictions 함수에 대한 테스트"""

    # Act, Assert
    assert get_predictions(query) == expected
