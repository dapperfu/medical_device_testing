"""Fixture for the hypertensive adult patient. Verifies: SSS008"""

import pytest

from medical_device_testing.humans.hypertensive_adult import HypertensiveAdult


@pytest.fixture
def hypertensive_adult() -> HypertensiveAdult:
    """Return a new hypertensive adult for this test. Verifies: SSS008"""
    return HypertensiveAdult()
