"""Pediatric mock patient. Implements: SSS002, SSS005"""

from medical_device_testing.humans.human import Human


class PediatricPatient(Human):
    """Child whose heart rate is inside pediatric limits and outside adult limits.

    Implements: SSS002, SSS005
    """

    def __init__(self, patient_id: str = "pediatric-patient") -> None:
        super().__init__(
            patient_id=patient_id,
            age_years=8,
            heart_rate_bpm=140,
            spo2_percent=98,
            systolic_mmhg=110,
            diastolic_mmhg=70,
            temperature_c=36.8,
            sensor_valid=True,
        )
