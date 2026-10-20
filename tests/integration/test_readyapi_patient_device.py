"""ReadyAPI client against the in-process app. Verifies: SSS012, SSS013, SSS006"""

from dataclasses import asdict

import pytest

from medical_device_testing.device.alarm_evaluator import Alarm
from medical_device_testing.device.patient_monitor import PatientMonitor
from medical_device_testing.device.patient_not_found import PatientNotFound
from medical_device_testing.device.readyapi_patient_device import ReadyApiPatientDevice
from medical_device_testing.humans.healthy_adult import HealthyAdult
from medical_device_testing.humans.pediatric_patient import PediatricPatient
from medical_device_testing.humans.sensor_fault_patient import SensorFaultPatient


def test_readyapi_device_returns_healthy_adult(
    readyapi_patient_device: ReadyApiPatientDevice, healthy_adult: HealthyAdult
) -> None:
    """The ReadyAPI device returns the healthy adult fields. Verifies: TD032, SSS012"""
    fetched = readyapi_patient_device.get_patient(healthy_adult.patient_id)
    assert asdict(fetched) == asdict(healthy_adult)


def test_readyapi_device_returns_pediatric_patient(
    readyapi_patient_device: ReadyApiPatientDevice, pediatric_patient: PediatricPatient
) -> None:
    """The ReadyAPI device returns the pediatric patient. Verifies: TD033, SSS012"""
    fetched = readyapi_patient_device.get_patient(pediatric_patient.patient_id)
    assert asdict(fetched) == asdict(pediatric_patient)


def test_readyapi_device_returns_sensor_fault(
    readyapi_patient_device: ReadyApiPatientDevice,
    sensor_fault_patient: SensorFaultPatient,
) -> None:
    """The ReadyAPI device preserves an invalid sensor. Verifies: TD034, SSS012"""
    fetched = readyapi_patient_device.get_patient(sensor_fault_patient.patient_id)
    assert fetched.sensor_valid is False
    assert fetched.heart_rate_bpm is None


def test_readyapi_device_unknown_patient_raises(
    readyapi_patient_device: ReadyApiPatientDevice,
) -> None:
    """An unknown ReadyAPI patient does not return a Human. Verifies: TD036, SSS013"""
    with pytest.raises(PatientNotFound):
        readyapi_patient_device.get_patient("missing-patient")


def test_readyapi_sensor_fault_still_alarms_on_monitor(
    readyapi_patient_device: ReadyApiPatientDevice,
    sensor_fault_patient: SensorFaultPatient,
    patient_monitor: PatientMonitor,
) -> None:
    """A patient fetched from ReadyAPI still trips the sensor-fault control.

    Verifies: TD037, SSS006, SSS012
    """
    fetched = readyapi_patient_device.get_patient(sensor_fault_patient.patient_id)
    patient_monitor.attach(fetched)
    patient_monitor.start()
    assert patient_monitor.vitals().valid is False
    assert patient_monitor.alarms() == frozenset({Alarm.SENSOR_FAULT})
