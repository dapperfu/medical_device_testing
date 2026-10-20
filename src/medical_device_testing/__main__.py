"""Print one reading from the healthy adult mock patient.

Implements: SSS001
"""

from medical_device_testing.device.patient_monitor import PatientMonitor
from medical_device_testing.humans.healthy_adult import HealthyAdult


def main() -> None:
    """Attach the healthy adult, start monitoring, and print the reading.

    Implements: SSS001
    """
    monitor = PatientMonitor()
    patient = HealthyAdult()
    monitor.attach(patient)
    monitor.start()
    reading = monitor.vitals()
    alarm_names = sorted(alarm.value for alarm in monitor.alarms())
    print(
        "patient="
        f"{patient.patient_id} valid={reading.valid} "
        f"hr={reading.heart_rate_bpm} spo2={reading.spo2_percent} "
        f"bp={reading.systolic_mmhg}/{reading.diastolic_mmhg} "
        f"temp={reading.temperature_c}"
    )
    print(f"alarms={alarm_names}")


if __name__ == "__main__":
    main()
