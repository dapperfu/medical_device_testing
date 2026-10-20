"""SOAP client against the local stub. Verifies: SSS010, SSS011, SSS006"""

from dataclasses import asdict

import pytest

from medical_device_testing.device.alarm_evaluator import Alarm
from medical_device_testing.device.patient_monitor import PatientMonitor
from medical_device_testing.device.patient_not_found import PatientNotFound
from medical_device_testing.device.soap_patient_device import SoapPatientDevice
from medical_device_testing.humans.healthy_adult import HealthyAdult
from medical_device_testing.humans.sensor_fault_patient import SensorFaultPatient


def test_soap_device_returns_healthy_adult(
    soap_patient_device: SoapPatientDevice, healthy_adult: HealthyAdult
) -> None:
    """The SOAP device returns the healthy adult fields. Verifies: TD028, SSS010"""
    fetched = soap_patient_device.get_patient(healthy_adult.patient_id)
    assert asdict(fetched) == asdict(healthy_adult)


def test_soap_device_returns_sensor_fault(
    soap_patient_device: SoapPatientDevice, sensor_fault_patient: SensorFaultPatient
) -> None:
    """The SOAP device preserves an invalid sensor. Verifies: TD029, SSS010"""
    fetched = soap_patient_device.get_patient(sensor_fault_patient.patient_id)
    assert asdict(fetched) == asdict(sensor_fault_patient)
    assert fetched.sensor_valid is False


def test_soap_device_unknown_patient_raises(
    soap_patient_device: SoapPatientDevice,
) -> None:
    """An unknown SOAP patient does not return a Human. Verifies: TD030, SSS011"""
    with pytest.raises(PatientNotFound):
        soap_patient_device.get_patient("missing-patient")


def test_soap_sensor_fault_still_alarms_on_monitor(
    soap_patient_device: SoapPatientDevice,
    sensor_fault_patient: SensorFaultPatient,
    patient_monitor: PatientMonitor,
) -> None:
    """A patient fetched over SOAP still trips the sensor-fault control.

    Verifies: TD035, SSS006, SSS010
    """
    fetched = soap_patient_device.get_patient(sensor_fault_patient.patient_id)
    patient_monitor.attach(fetched)
    patient_monitor.start()
    assert patient_monitor.vitals().valid is False
    assert patient_monitor.alarms() == frozenset({Alarm.SENSOR_FAULT})
