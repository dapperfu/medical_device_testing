"""Fixture for the mock patient monitor. Verifies: SSS008"""

import pytest

from medical_device_testing.device.patient_monitor import PatientMonitor


@pytest.fixture
def patient_monitor() -> PatientMonitor:
    """Return a new idle monitor for this test. Verifies: SSS008"""
    return PatientMonitor()
