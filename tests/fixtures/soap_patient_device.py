"""Fixture for the SOAP patient client. Verifies: SSS010"""

import pytest

from medical_device_testing.device.soap_patient_device import SoapPatientDevice
from medical_device_testing.device.soap_patient_service import SoapPatientService


@pytest.fixture
def soap_patient_device(soap_patient_service: SoapPatientService) -> SoapPatientDevice:
    """Return a client pointed at this test's SOAP stub. Verifies: SSS010"""
    return SoapPatientDevice(soap_patient_service.endpoint)
