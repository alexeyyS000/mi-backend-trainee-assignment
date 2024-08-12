"""
Testcases for datetime utils.
"""
from datetime import datetime

import pytest

from utils.datetime import get_uts_from_datetime


@pytest.mark.parametrize('dt,expected', [
    (datetime(1970, 1, 1, 0, 0, 0, 0), 0)
])
def test_get_uts_from_datetime(dt: datetime, expected: int):
    actual = get_uts_from_datetime(dt)
    assert actual == expected
