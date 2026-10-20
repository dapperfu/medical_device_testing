"""Software system tests. Each SSS requirement is exercised here.

Verifies: SSS001, SSS002, SSS003, SSS004, SSS005, SSS006, SSS007, SSS008, SSS009
"""

import pytest

from medical_device_testing.device.alarm_evaluator import Alarm
from medical_device_testing.device.alarm_limits import AlarmLimits, LimitRejected
from medical_device_testing.device.patient_monitor import NoPatient, PatientMonitor
from medical_device_testing.humans.healthy_adult import HealthyAdult
from medical_device_testing.humans.human import Human
from medical_device_testing.humans.pediatric_patient import PediatricPatient
from medical_device_testing.humans.sensor_fault_patient import SensorFaultPatient

_PATIENT_FIXTURES = (
    "healthy_adult",
    "tachycardic_adult",
    "hypoxic_adult",
    "hypertensive_adult",
    "pediatric_patient",
    "sensor_fault_patient",
    "patient_monitor",
)


def test_system_reports_attached_vitals(
    patient_monitor: PatientMonitor, healthy_adult: HealthyAdult
) -> None:
    """The running monitor presents the five attached vital values. Verifies: SSS001"""
    patient_monitor.attach(healthy_adult)
    patient_monitor.start()
    reading = patient_monitor.vitals()
    assert reading == patient_monitor.vitals()
    assert (
        reading.valid,
        reading.heart_rate_bpm,
        reading.spo2_percent,
        reading.systolic_mmhg,
        reading.diastolic_mmhg,
        reading.temperature_c,
    ) == (True, 72, 98, 118, 76, 36.8)


def test_system_profile_follows_age(
    patient_monitor: PatientMonitor,
    healthy_adult: HealthyAdult,
    pediatric_patient: PediatricPatient,
) -> None:
    """Adult and pediatric patients select different profiles. Verifies: SSS002"""
    patient_monitor.attach(healthy_adult)
    patient_monitor.start()
    assert patient_monitor.limits == AlarmLimits.adult_defaults()
    assert patient_monitor.alarms() == frozenset()

    patient_monitor.attach(pediatric_patient)
    assert patient_monitor.limits == AlarmLimits.pediatric_defaults()
    assert Alarm.HEART_RATE not in patient_monitor.alarms()


def test_system_boundary_value_does_not_alarm(patient_monitor: PatientMonitor) -> None:
    """Heart rate equal to the adult high limit does not alarm. Verifies: SSS003"""
    on_limit = Human("system-boundary", 40, 120, 98, 118, 76, 36.8, True)
    one_past = Human("system-past", 40, 121, 98, 118, 76, 36.8, True)
    patient_monitor.attach(on_limit)
    patient_monitor.start()
    assert Alarm.HEART_RATE not in patient_monitor.alarms()
    patient_monitor.attach(one_past)
    assert patient_monitor.alarms() == frozenset({Alarm.HEART_RATE})


def test_system_start_and_stop(patient_monitor: PatientMonitor) -> None:
    """Start without a patient is rejected. Stop clears alarms. Verifies: SSS004"""
    with pytest.raises(NoPatient):
        patient_monitor.start()
    assert patient_monitor.running is False
    patient_monitor.attach(Human("running", 40, 140, 98, 118, 76, 36.8, True))
    patient_monitor.start()
    assert patient_monitor.alarms() == frozenset({Alarm.HEART_RATE})
    patient_monitor.stop()
    assert patient_monitor.vitals().valid is False
    assert patient_monitor.alarms() == frozenset()


def test_system_attach_stores_patient_and_profile(
    patient_monitor: PatientMonitor, pediatric_patient: PediatricPatient
) -> None:
    """attach stores the patient and selects the pediatric profile. Verifies: SSS005"""
    patient_monitor.attach(pediatric_patient)
    assert patient_monitor.patient is pediatric_patient
    assert patient_monitor.limits == AlarmLimits.pediatric_defaults()


def test_system_sensor_fault(
    patient_monitor: PatientMonitor, sensor_fault_patient: SensorFaultPatient
) -> None:
    """Invalid sensor raises only SENSOR_FAULT and hides vitals. Verifies: SSS006"""
    patient_monitor.attach(sensor_fault_patient)
    patient_monitor.start()
    assert patient_monitor.vitals().valid is False
    assert patient_monitor.alarms() == frozenset({Alarm.SENSOR_FAULT})


def test_system_rejects_out_of_range_command(
    patient_monitor: PatientMonitor, healthy_adult: HealthyAdult
) -> None:
    """A rejected limit command is not used for alarm evaluation. Verifies: SSS007"""
    patient_monitor.attach(healthy_adult)
    before = patient_monitor.limits
    with pytest.raises(LimitRejected):
        patient_monitor.set_limits(AlarmLimits(50, 120, -1, 160, 100, 35.0, 38.0))
    patient_monitor.start()
    assert patient_monitor.limits == before
    assert patient_monitor.alarms() == frozenset()


def test_fixtures_are_function_scoped(request: pytest.FixtureRequest) -> None:
    """Each required fixture is function scoped and builds a new object.

    Verifies: SSS008
    """
    manager = request.session._fixturemanager
    for name in _PATIENT_FIXTURES:
        definitions = manager.getfixturedefs(name, request.node)
        assert definitions is not None
        assert definitions[-1].scope == "function"
        first = request.getfixturevalue(name)
        assert first is not None
