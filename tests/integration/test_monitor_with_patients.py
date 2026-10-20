"""Integration of PatientMonitor with each mock patient fixture.

Verifies: SSS001, SSS002, SSS004, SSS005, SSS006, SSS007
"""

import pytest

from medical_device_testing.device.alarm_evaluator import Alarm
from medical_device_testing.device.alarm_limits import AlarmLimits, LimitRejected
from medical_device_testing.device.patient_monitor import PatientMonitor
from medical_device_testing.humans.healthy_adult import HealthyAdult
from medical_device_testing.humans.human import Human
from medical_device_testing.humans.hypertensive_adult import HypertensiveAdult
from medical_device_testing.humans.hypoxic_adult import HypoxicAdult
from medical_device_testing.humans.pediatric_patient import PediatricPatient
from medical_device_testing.humans.sensor_fault_patient import SensorFaultPatient
from medical_device_testing.humans.tachycardic_adult import TachycardicAdult


def _started(monitor: PatientMonitor, patient: Human) -> PatientMonitor:
    monitor.attach(patient)
    monitor.start()
    return monitor


def test_healthy_adult_reports_vitals_and_no_alarm(
    patient_monitor: PatientMonitor, healthy_adult: HealthyAdult
) -> None:
    """A running healthy adult is presented unchanged and without alarms.

    Verifies: SSS001, SSS002, SSS005
    """
    _started(patient_monitor, healthy_adult)
    reading = patient_monitor.vitals()
    assert reading.valid is True
    assert reading.heart_rate_bpm == 72
    assert reading.spo2_percent == 98
    assert reading.systolic_mmhg == 118
    assert reading.diastolic_mmhg == 76
    assert reading.temperature_c == 36.8
    assert patient_monitor.alarms() == frozenset()
    assert patient_monitor.limits == AlarmLimits.adult_defaults()


def test_tachycardic_adult_heart_rate_alarm(
    patient_monitor: PatientMonitor, tachycardic_adult: TachycardicAdult
) -> None:
    """The tachycardic adult raises only HEART_RATE. Verifies: SSS002"""
    _started(patient_monitor, tachycardic_adult)
    assert patient_monitor.alarms() == frozenset({Alarm.HEART_RATE})


def test_hypoxic_adult_spo2_alarm(
    patient_monitor: PatientMonitor, hypoxic_adult: HypoxicAdult
) -> None:
    """The hypoxic adult raises only SPO2. Verifies: SSS002"""
    _started(patient_monitor, hypoxic_adult)
    assert patient_monitor.alarms() == frozenset({Alarm.SPO2})


def test_hypertensive_adult_blood_pressure_alarm(
    patient_monitor: PatientMonitor, hypertensive_adult: HypertensiveAdult
) -> None:
    """The hypertensive adult raises only BLOOD_PRESSURE. Verifies: SSS002"""
    _started(patient_monitor, hypertensive_adult)
    assert patient_monitor.alarms() == frozenset({Alarm.BLOOD_PRESSURE})


def test_pediatric_patient_uses_pediatric_profile(
    patient_monitor: PatientMonitor, pediatric_patient: PediatricPatient
) -> None:
    """Heart rate 140 does not alarm when the pediatric profile is selected.

    Verifies: SSS002, SSS005
    """
    _started(patient_monitor, pediatric_patient)
    assert patient_monitor.limits == AlarmLimits.pediatric_defaults()
    assert patient_monitor.alarms() == frozenset()


def test_sensor_fault_patient_hides_vitals(
    patient_monitor: PatientMonitor, sensor_fault_patient: SensorFaultPatient
) -> None:
    """A sensor fault does not present numeric vitals. Verifies: SSS006"""
    _started(patient_monitor, sensor_fault_patient)
    assert patient_monitor.vitals().valid is False
    assert patient_monitor.alarms() == frozenset({Alarm.SENSOR_FAULT})


def test_rejected_limits_leave_the_adult_profile(
    patient_monitor: PatientMonitor, healthy_adult: HealthyAdult
) -> None:
    """An out-of-range command does not replace the profile selected at attach.

    Verifies: SSS007
    """
    patient_monitor.attach(healthy_adult)
    rejected = AlarmLimits(50, 120, 101, 160, 100, 35.0, 38.0)
    with pytest.raises(LimitRejected):
        patient_monitor.set_limits(rejected)
    patient_monitor.start()
    assert patient_monitor.limits == AlarmLimits.adult_defaults()
    assert patient_monitor.alarms() == frozenset()


def test_idle_and_stopped_monitor_has_no_alarms(
    patient_monitor: PatientMonitor, tachycardic_adult: TachycardicAdult
) -> None:
    """Alarms and valid vitals appear only while monitoring is running.

    Verifies: SSS004
    """
    assert patient_monitor.vitals().valid is False
    assert patient_monitor.alarms() == frozenset()
    patient_monitor.attach(tachycardic_adult)
    assert patient_monitor.alarms() == frozenset()
    patient_monitor.start()
    assert patient_monitor.alarms() == frozenset({Alarm.HEART_RATE})
    patient_monitor.stop()
    assert patient_monitor.vitals().valid is False
    assert patient_monitor.alarms() == frozenset()
