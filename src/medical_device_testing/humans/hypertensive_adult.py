"""Hypertensive adult mock patient. Implements: SSS002"""

from medical_device_testing.humans.human import Human


class HypertensiveAdult(Human):
    """Adult whose systolic pressure is above the adult limit. Implements: SSS002"""

    def __init__(self, patient_id: str = "hypertensive-adult") -> None:
        super().__init__(
            patient_id=patient_id,
            age_years=55,
            heart_rate_bpm=78,
            spo2_percent=97,
            systolic_mmhg=180,
            diastolic_mmhg=95,
            temperature_c=36.8,
            sensor_valid=True,
        )
