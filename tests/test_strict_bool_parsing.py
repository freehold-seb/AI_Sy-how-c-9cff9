import pytest

from agent_core.config import parse_bool


@pytest.mark.parametrize("value", ["true", "TRUE", "True"])
def test_parse_bool_true(value):
    assert parse_bool(value) is True


@pytest.mark.parametrize("value", ["false", "FALSE", "False"])
def test_parse_bool_false(value):
    assert parse_bool(value) is False


@pytest.mark.parametrize("value", ["yes", "no", "0", "anything else"])
def test_parse_bool_rejects_invalid_strings(value):
    with pytest.raises(ValueError):
        parse_bool(value)


@pytest.mark.parametrize("value", [1, None])
def test_parse_bool_rejects_non_strings(value):
    with pytest.raises(TypeError):
        parse_bool(value)
