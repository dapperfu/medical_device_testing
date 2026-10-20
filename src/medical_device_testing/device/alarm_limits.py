"""Alarm limit profiles and rejection of out-of-range commands.

Implements: SSS002, SSS007
"""

from dataclasses import dataclass

from medical_device_testing.humans.human import Human


class LimitRejected(Exception):
    """The alarm-limit command was outside the allowed range.

    Implements: SSS007
    """


@dataclass(frozen=True)
class AlarmLimits:
    """Inclusive vital-sign limits. A value equal to a limit does not alarm.

    Implements: SSS002, SSS003, SSS007
    """

    hr_low: int
    hr_high: int
    spo2_low: int
    systolic_high: int
    diastolic_high: int
    temp_low: float
    temp_high: float

    @staticmethod
    def adult_defaults() -> "AlarmLimits":
        """Return the adult profile. Implements: SSS002"""
        return AlarmLimits(
            hr_low=50,
            hr_high=120,
            spo2_low=90,
            systolic_high=160,
            diastolic_high=100,
            temp_low=35.0,
            temp_high=38.0,
        )

    @staticmethod
    def pediatric_defaults() -> "AlarmLimits":
        """Return the pediatric profile. Implements: SSS002"""
        return AlarmLimits(
            hr_low=70,
            hr_high=160,
            spo2_low=92,
            systolic_high=120,
            diastolic_high=80,
            temp_low=35.5,
            temp_high=38.0,
        )

    @staticmethod
    def for_age(age_years: int) -> "AlarmLimits":
        """Select the profile from age. Age 18 and older is adult.

        Implements: SSS002, SSS005
        """
        if age_years < 18:
            return AlarmLimits.pediatric_defaults()
        return AlarmLimits.adult_defaults()

    @staticmethod
    def for_patient(patient: Human) -> "AlarmLimits":
        """Select the profile for an attached patient. Implements: SSS005"""
        return AlarmLimits.for_age(patient.age_years)


def accept_limits(limits: AlarmLimits) -> None:
    """Raise LimitRejected when the command is outside the allowed range.

    On rejection the caller must leave the previously accepted limits in place.
    Implements: SSS007
    """
    reasons: list[str] = []
    if not 20 <= limits.hr_low <= 200:
        reasons.append("heart-rate low limit must be from 20 through 200")
    if not 30 <= limits.hr_high <= 250:
        reasons.append("heart-rate high limit must be from 30 through 250")
    if limits.hr_high <= limits.hr_low:
        reasons.append("heart-rate high limit must be greater than the low limit")
    if not 50 <= limits.spo2_low <= 100:
        reasons.append("SpO2 low limit must be from 50 through 100")
    if not 80 <= limits.systolic_high <= 250:
        reasons.append("systolic high limit must be from 80 through 250")
    if not 40 <= limits.diastolic_high <= 150:
        reasons.append("diastolic high limit must be from 40 through 150")
    if not 30.0 <= limits.temp_low <= 43.0:
        reasons.append("temperature low limit must be from 30.0 through 43.0")
    if not 30.0 <= limits.temp_high <= 43.0:
        reasons.append("temperature high limit must be from 30.0 through 43.0")
    if limits.temp_high <= limits.temp_low:
        reasons.append("temperature high limit must be greater than the low limit")
    if reasons:
        raise LimitRejected("; ".join(reasons))
