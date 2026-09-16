import math

import pytest

from verifier import validate_score


def test_accepts_finite_scores():
    assert validate_score(0.0) is True
    assert validate_score(1.5) is True
    assert validate_score(-2.3) is True


def test_rejects_nan():
    assert validate_score(math.nan) is False


def test_rejects_infinite():
    assert validate_score(math.inf) is False
    assert validate_score(-math.inf) is False


@pytest.mark.parametrize("value", ["not a number", None])
def test_rejects_non_numeric(value):
    with pytest.raises(TypeError):
        validate_score(value)
