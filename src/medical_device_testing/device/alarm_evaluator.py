"""Pure alarm evaluation from a patient stimulus and a limit profile.

Implements: SSS002, SSS003, SSS006
"""

from enum import Enum

from medical_device_testing.device.alarm_limits import AlarmLimits
from medical_device_testing.humans.human import Human


class Alarm(Enum):
    """Alarm identifiers reported by the monitor."""

    HEART_RATE = "HEART_RATE"
    SPO2 = "SPO2"
    BLOOD_PRESSURE = "BLOOD_PRESSURE"
    TEMPERATURE = "TEMPERATURE"
    SENSOR_FAULT = "SENSOR_FAULT"


def evaluate(patient: Human, limits: AlarmLimits) -> frozenset[Alarm]:
    """Return the alarms for one patient and one accepted limit profile.

    An invalid sensor produces only SENSOR_FAULT. A vital equal to its limit
    does not alarm. Missing numbers on a valid sensor do not alarm.
    Implements: SSS002, SSS003, SSS006
    """
    if not patient.sensor_valid:
        return frozenset({Alarm.SENSOR_FAULT})

    alarms: set[Alarm] = set()
    heart_rate = patient.heart_rate_bpm
    if heart_rate is not None and (
        heart_rate < limits.hr_low or heart_rate > limits.hr_high
    ):
        alarms.add(Alarm.HEART_RATE)

    spo2 = patient.spo2_percent
    if spo2 is not None and spo2 < limits.spo2_low:
        alarms.add(Alarm.SPO2)

    systolic = patient.systolic_mmhg
    diastolic = patient.diastolic_mmhg
    if (systolic is not None and systolic > limits.systolic_high) or (
        diastolic is not None and diastolic > limits.diastolic_high
    ):
        alarms.add(Alarm.BLOOD_PRESSURE)

    temperature = patient.temperature_c
    if temperature is not None and (
        temperature < limits.temp_low or temperature > limits.temp_high
    ):
        alarms.add(Alarm.TEMPERATURE)

    return frozenset(alarms)
