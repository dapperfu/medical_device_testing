"""Fixture for the healthy adult patient. Verifies: SSS008"""

import pytest

from medical_device_testing.humans.healthy_adult import HealthyAdult


@pytest.fixture
def healthy_adult() -> HealthyAdult:
    """Return a new healthy adult for this test. Verifies: SSS008"""
    return HealthyAdult()
