"""Unit tests for alarm evaluation boundaries and sensor fault.

Verifies: SSS002, SSS003, SSS006
"""

from medical_device_testing.device.alarm_evaluator import Alarm, evaluate
from medical_device_testing.device.alarm_limits import AlarmLimits
from medical_device_testing.humans.human import Human
from medical_device_testing.humans.sensor_fault_patient import SensorFaultPatient


def _adult(
    heart_rate: int = 72,
    spo2: int = 98,
    systolic: int = 118,
    diastolic: int = 76,
    temperature: float = 36.8,
) -> Human:
    return Human(
        "unit-adult",
        40,
        heart_rate,
        spo2,
        systolic,
        diastolic,
        temperature,
        True,
    )


def test_equal_to_limit_does_not_alarm() -> None:
    """Values equal to adult limits do not alarm. Verifies: SSS003"""
    limits = AlarmLimits.adult_defaults()
    on_limit = Human("on-limit", 40, 120, 90, 160, 100, 38.0, True)
    low_edge = Human("low-edge", 40, 50, 90, 160, 100, 35.0, True)
    assert evaluate(on_limit, limits) == frozenset()
    assert evaluate(low_edge, limits) == frozenset()


def test_one_past_adult_limits_alarms() -> None:
    """One step outside each adult limit raises that alarm. Verifies: SSS002, SSS003"""
    limits = AlarmLimits.adult_defaults()
    assert evaluate(_adult(heart_rate=121), limits) == frozenset({Alarm.HEART_RATE})
    assert evaluate(_adult(heart_rate=49), limits) == frozenset({Alarm.HEART_RATE})
    assert evaluate(_adult(spo2=89), limits) == frozenset({Alarm.SPO2})
    assert evaluate(_adult(systolic=161), limits) == frozenset({Alarm.BLOOD_PRESSURE})
    assert evaluate(_adult(diastolic=101), limits) == frozenset({Alarm.BLOOD_PRESSURE})
    assert evaluate(_adult(temperature=38.1), limits) == frozenset({Alarm.TEMPERATURE})
    assert evaluate(_adult(temperature=34.9), limits) == frozenset({Alarm.TEMPERATURE})


def test_pediatric_limits_differ_from_adult() -> None:
    """SpO2 91 alarms on the pediatric profile and not on the adult profile.

    Verifies: SSS002
    """
    patient = _adult(spo2=91, heart_rate=140)
    assert Alarm.SPO2 not in evaluate(patient, AlarmLimits.adult_defaults())
    assert Alarm.HEART_RATE in evaluate(patient, AlarmLimits.adult_defaults())
    pediatric = evaluate(patient, AlarmLimits.pediatric_defaults())
    assert pediatric == frozenset({Alarm.SPO2})


def test_sensor_fault_suppresses_vital_alarms() -> None:
    """An invalid sensor raises only SENSOR_FAULT. Verifies: SSS006"""
    assert evaluate(SensorFaultPatient(), AlarmLimits.adult_defaults()) == frozenset(
        {Alarm.SENSOR_FAULT}
    )
