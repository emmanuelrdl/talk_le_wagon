import os
import pandas as pd
from unittest.mock import patch
import pytest
from contextlib import contextmanager
import logic.main
from logic.main import apply_business_opportunities


@pytest.fixture
def prospects_calendar():
    df = pd.read_csv(
        os.path.dirname(os.path.abspath(__file__)) + "/./inputs/prospects_calendar.csv"
    )
    return df


@contextmanager
def mock(prospects_calendar):
    with (
        patch.object(
            logic.main,
            "get_prospects_calendar",
            return_value=prospects_calendar,
        )
    ):
        yield


def expected_proceed_calendar():
    df = pd.read_csv(
        os.path.dirname(os.path.abspath(__file__))
        + "/./outputs/proceed_prospects_calendar.csv"
    )
    return df


def test_assert():
    assert 1 == 1


def test_get_opportunties(prospects_calendar):
    with mock(prospects_calendar) as _:
        df = apply_business_opportunities(prospects_calendar)
        expected_df = expected_proceed_calendar()
        assert len(df) == df.prospect_name.nunique() * 52
        assert df.equals(expected_df)
