"""Fixture for the ReadyAPI patient service and client. Verifies: SSS012"""

import pytest
from readyapi.testclient import TestClient

from medical_device_testing.device.readyapi_patient_device import ReadyApiPatientDevice
from medical_device_testing.device.readyapi_patient_service import create_readyapi_app
from medical_device_testing.humans.healthy_adult import HealthyAdult
from medical_device_testing.humans.hypertensive_adult import HypertensiveAdult
from medical_device_testing.humans.hypoxic_adult import HypoxicAdult
from medical_device_testing.humans.pediatric_patient import PediatricPatient
from medical_device_testing.humans.sensor_fault_patient import SensorFaultPatient
from medical_device_testing.humans.tachycardic_adult import TachycardicAdult


@pytest.fixture
def readyapi_patient_device(
    healthy_adult: HealthyAdult,
    tachycardic_adult: TachycardicAdult,
    hypoxic_adult: HypoxicAdult,
    hypertensive_adult: HypertensiveAdult,
    pediatric_patient: PediatricPatient,
    sensor_fault_patient: SensorFaultPatient,
) -> ReadyApiPatientDevice:
    """Serve the mock patients on a ReadyAPI app and return its client.

    Verifies: SSS012
    """
    patients = {
        patient.patient_id: patient
        for patient in (
            healthy_adult,
            tachycardic_adult,
            hypoxic_adult,
            hypertensive_adult,
            pediatric_patient,
            sensor_fault_patient,
        )
    }
    app = create_readyapi_app(patients)
    client = TestClient(app)
    return ReadyApiPatientDevice(client)
