"""Fixture for the pediatric patient. Verifies: SSS008"""

import pytest

from medical_device_testing.humans.pediatric_patient import PediatricPatient


@pytest.fixture
def pediatric_patient() -> PediatricPatient:
    """Return a new pediatric patient for this test. Verifies: SSS008"""
    return PediatricPatient()
