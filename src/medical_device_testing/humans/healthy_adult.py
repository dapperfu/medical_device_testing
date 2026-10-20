"""Healthy adult mock patient. Implements: SSS001, SSS002"""

from medical_device_testing.humans.human import Human


class HealthyAdult(Human):
    """Adult with every vital inside the adult limits. Implements: SSS001"""

    def __init__(self, patient_id: str = "healthy-adult") -> None:
        super().__init__(
            patient_id=patient_id,
            age_years=35,
            heart_rate_bpm=72,
            spo2_percent=98,
            systolic_mmhg=118,
            diastolic_mmhg=76,
            temperature_c=36.8,
            sensor_valid=True,
        )
