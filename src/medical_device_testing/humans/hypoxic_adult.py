"""Hypoxic adult mock patient. Implements: SSS002"""

from medical_device_testing.humans.human import Human


class HypoxicAdult(Human):
    """Adult whose oxygen saturation is below the adult low limit. Implements: SSS002"""

    def __init__(self, patient_id: str = "hypoxic-adult") -> None:
        super().__init__(
            patient_id=patient_id,
            age_years=60,
            heart_rate_bpm=88,
            spo2_percent=85,
            systolic_mmhg=122,
            diastolic_mmhg=80,
            temperature_c=36.7,
            sensor_valid=True,
        )
