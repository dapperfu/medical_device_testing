"""Unit tests for Human and the mock patient subclasses.

Verifies: SSS002, SSS008
"""

from medical_device_testing.humans.healthy_adult import HealthyAdult
from medical_device_testing.humans.human import Human
from medical_device_testing.humans.hypertensive_adult import HypertensiveAdult
from medical_device_testing.humans.hypoxic_adult import HypoxicAdult
from medical_device_testing.humans.pediatric_patient import PediatricPatient
from medical_device_testing.humans.sensor_fault_patient import SensorFaultPatient
from medical_device_testing.humans.tachycardic_adult import TachycardicAdult


def test_age_selects_population() -> None:
    """Age 18 is adult and age 17 is pediatric. Verifies: SSS002"""
    adult = Human("adult-edge", 18, 72, 98, 118, 76, 36.8, True)
    child = Human("child-edge", 17, 110, 98, 100, 60, 36.8, True)
    assert adult.is_pediatric is False
    assert child.is_pediatric is True


def test_mock_patients_inherit_from_human() -> None:
    """Each mock patient is a Human. Verifies: SSS002, SSS008"""
    patients = [
        HealthyAdult(),
        TachycardicAdult(),
        HypoxicAdult(),
        HypertensiveAdult(),
        PediatricPatient(),
        SensorFaultPatient(),
    ]
    assert all(isinstance(patient, Human) for patient in patients)
    assert PediatricPatient().age_years == 8
    assert SensorFaultPatient().sensor_valid is False
    assert SensorFaultPatient().heart_rate_bpm is None
