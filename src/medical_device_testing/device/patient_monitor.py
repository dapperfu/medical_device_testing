"""Mock vital-signs patient monitor.

Implements: SSS001, SSS004, SSS005, SSS006, SSS007
"""

from dataclasses import dataclass

from medical_device_testing.device.alarm_evaluator import Alarm, evaluate
from medical_device_testing.device.alarm_limits import AlarmLimits, accept_limits
from medical_device_testing.humans.human import Human


class NoPatient(Exception):
    """Monitoring was started with no patient attached. Implements: SSS004"""


@dataclass(frozen=True)
class VitalsReading:
    """Vitals presented to the operator. Implements: SSS001"""

    valid: bool
    heart_rate_bpm: int | None
    spo2_percent: int | None
    systolic_mmhg: int | None
    diastolic_mmhg: int | None
    temperature_c: float | None


class PatientMonitor:
    """Software item that attaches a patient, applies limits, and reports alarms.

    No segregation from the rest of this package is claimed. This item stays
    at the same class as the software system.
    Implements: SSS001, SSS004, SSS005, SSS007
    """

    def __init__(self) -> None:
        self._patient: Human | None = None
        self._limits: AlarmLimits = AlarmLimits.adult_defaults()
        self._running: bool = False

    @property
    def patient(self) -> Human | None:
        """Return the attached patient, if any. Implements: SSS005"""
        return self._patient

    @property
    def limits(self) -> AlarmLimits:
        """Return the limits currently in effect. Implements: SSS007"""
        return self._limits

    @property
    def running(self) -> bool:
        """Return True while monitoring is started. Implements: SSS004"""
        return self._running

    def attach(self, patient: Human) -> None:
        """Store the patient and select that patient's default profile.

        Implements: SSS005
        """
        self._patient = patient
        self._limits = AlarmLimits.for_patient(patient)

    def start(self) -> None:
        """Begin monitoring. Reject a start when no patient is attached.

        Implements: SSS004
        """
        if self._patient is None:
            raise NoPatient("A patient must be attached before monitoring starts")
        self._running = True

    def stop(self) -> None:
        """End monitoring. Implements: SSS004"""
        self._running = False

    def set_limits(self, limits: AlarmLimits) -> None:
        """Apply an in-range limit command. Leave current limits on rejection.

        Implements: SSS007
        """
        accept_limits(limits)
        self._limits = limits

    def vitals(self) -> VitalsReading:
        """Present vitals only while running with a valid sensor.

        Implements: SSS001, SSS004, SSS006
        """
        patient = self._patient
        if not self._running or patient is None or not patient.sensor_valid:
            return VitalsReading(
                valid=False,
                heart_rate_bpm=None,
                spo2_percent=None,
                systolic_mmhg=None,
                diastolic_mmhg=None,
                temperature_c=None,
            )
        return VitalsReading(
            valid=True,
            heart_rate_bpm=patient.heart_rate_bpm,
            spo2_percent=patient.spo2_percent,
            systolic_mmhg=patient.systolic_mmhg,
            diastolic_mmhg=patient.diastolic_mmhg,
            temperature_c=patient.temperature_c,
        )

    def alarms(self) -> frozenset[Alarm]:
        """Return active alarms. The set is empty when monitoring is stopped.

        Implements: SSS002, SSS004, SSS006
        """
        patient = self._patient
        if not self._running or patient is None:
            return frozenset()
        return evaluate(patient, self._limits)


__all__ = [
    "Alarm",
    "AlarmLimits",
    "NoPatient",
    "PatientMonitor",
    "VitalsReading",
]
