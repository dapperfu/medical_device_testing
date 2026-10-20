"""Patient stimulus. Alarm decisions stay in the monitor, not in this type.

Implements: SSS002, SSS005
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Human:
    """A person attached to the mock monitor.

    Implements: SSS002, SSS005
    """

    patient_id: str
    age_years: int
    heart_rate_bpm: int | None
    spo2_percent: int | None
    systolic_mmhg: int | None
    diastolic_mmhg: int | None
    temperature_c: float | None
    sensor_valid: bool = True

    @property
    def is_pediatric(self) -> bool:
        """Return True when the pediatric limit profile applies.

        Implements: SSS002
        """
        return self.age_years < 18
