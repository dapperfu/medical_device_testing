"""Tachycardic adult mock patient. Implements: SSS002"""

from medical_device_testing.humans.human import Human


class TachycardicAdult(Human):
    """Adult whose heart rate is above the adult high limit. Implements: SSS002"""

    def __init__(self, patient_id: str = "tachycardic-adult") -> None:
        super().__init__(
            patient_id=patient_id,
            age_years=45,
            heart_rate_bpm=140,
            spo2_percent=97,
            systolic_mmhg=124,
            diastolic_mmhg=78,
            temperature_c=36.9,
            sensor_valid=True,
        )
