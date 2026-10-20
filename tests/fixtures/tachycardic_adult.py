"""Fixture for the tachycardic adult patient. Verifies: SSS008"""

import pytest

from medical_device_testing.humans.tachycardic_adult import TachycardicAdult


@pytest.fixture
def tachycardic_adult() -> TachycardicAdult:
    """Return a new tachycardic adult for this test. Verifies: SSS008"""
    return TachycardicAdult()
