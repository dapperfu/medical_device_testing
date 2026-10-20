"""Sensor-fault mock patient. Implements: SSS006"""

from medical_device_testing.humans.human import Human


class SensorFaultPatient(Human):
    """Patient whose sensor reading is invalid. Implements: SSS006"""

    def __init__(self, patient_id: str = "sensor-fault-patient") -> None:
        super().__init__(
            patient_id=patient_id,
            age_years=40,
            heart_rate_bpm=None,
            spo2_percent=None,
            systolic_mmhg=None,
            diastolic_mmhg=None,
            temperature_c=None,
            sensor_valid=False,
        )
