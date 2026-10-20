"""Fixture for the local SOAP patient stub. Verifies: SSS010"""

import pytest

from medical_device_testing.device.soap_patient_service import SoapPatientService
from medical_device_testing.humans.healthy_adult import HealthyAdult
from medical_device_testing.humans.hypertensive_adult import HypertensiveAdult
from medical_device_testing.humans.hypoxic_adult import HypoxicAdult
from medical_device_testing.humans.pediatric_patient import PediatricPatient
from medical_device_testing.humans.sensor_fault_patient import SensorFaultPatient
from medical_device_testing.humans.tachycardic_adult import TachycardicAdult


@pytest.fixture
def soap_patient_service(
    healthy_adult: HealthyAdult,
    tachycardic_adult: TachycardicAdult,
    hypoxic_adult: HypoxicAdult,
    hypertensive_adult: HypertensiveAdult,
    pediatric_patient: PediatricPatient,
    sensor_fault_patient: SensorFaultPatient,
) -> SoapPatientService:
    """Serve the mock patients over SOAP and stop the stub after the test.

    Verifies: SSS010
    """
    service = SoapPatientService()
    for patient in (
        healthy_adult,
        tachycardic_adult,
        hypoxic_adult,
        hypertensive_adult,
        pediatric_patient,
        sensor_fault_patient,
    ):
        service.register(patient)
    yield service
    service.close()
