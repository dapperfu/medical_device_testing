"""Fixture for the sensor-fault patient. Verifies: SSS008"""

import pytest

from medical_device_testing.humans.sensor_fault_patient import SensorFaultPatient


@pytest.fixture
def sensor_fault_patient() -> SensorFaultPatient:
    """Return a new sensor-fault patient for this test. Verifies: SSS008"""
    return SensorFaultPatient()
