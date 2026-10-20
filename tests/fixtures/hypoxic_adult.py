"""Fixture for the hypoxic adult patient. Verifies: SSS008"""

import pytest

from medical_device_testing.humans.hypoxic_adult import HypoxicAdult


@pytest.fixture
def hypoxic_adult() -> HypoxicAdult:
    """Return a new hypoxic adult for this test. Verifies: SSS008"""
    return HypoxicAdult()
