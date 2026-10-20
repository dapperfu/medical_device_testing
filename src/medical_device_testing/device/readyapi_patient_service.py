"""ReadyAPI service that returns a registered Human as JSON.

Implements: SSS012, SSS013, IRS006
"""

from collections.abc import Mapping

from readyapi import HTTPException, ReadyAPI

from medical_device_testing.humans.human import Human


def human_to_document(patient: Human) -> dict[str, object]:
    """JSON document for one patient. Implements: SSS012"""
    return {
        "patient_id": patient.patient_id,
        "age_years": patient.age_years,
        "heart_rate_bpm": patient.heart_rate_bpm,
        "spo2_percent": patient.spo2_percent,
        "systolic_mmhg": patient.systolic_mmhg,
        "diastolic_mmhg": patient.diastolic_mmhg,
        "temperature_c": patient.temperature_c,
        "sensor_valid": patient.sensor_valid,
    }


def human_from_document(document: Mapping[str, object]) -> Human:
    """Build a Human from the ReadyAPI JSON document. Implements: SSS012"""

    def optional_int(name: str) -> int | None:
        value = document.get(name)
        if value is None:
            return None
        return int(value)  # type: ignore[arg-type]

    def optional_float(name: str) -> float | None:
        value = document.get(name)
        if value is None:
            return None
        return float(value)  # type: ignore[arg-type]

    return Human(
        patient_id=str(document["patient_id"]),
        age_years=int(document["age_years"]),  # type: ignore[arg-type]
        heart_rate_bpm=optional_int("heart_rate_bpm"),
        spo2_percent=optional_int("spo2_percent"),
        systolic_mmhg=optional_int("systolic_mmhg"),
        diastolic_mmhg=optional_int("diastolic_mmhg"),
        temperature_c=optional_float("temperature_c"),
        sensor_valid=bool(document["sensor_valid"]),
    )


def create_readyapi_app(patients: dict[str, Human]) -> ReadyAPI:
    """Build the patient resource. Implements: SSS012, SSS013"""
    app = ReadyAPI()

    @app.get("/patients/{patient_id}")
    def read_patient(patient_id: str) -> dict[str, object]:
        patient = patients.get(patient_id)
        if patient is None:
            raise HTTPException(status_code=404, detail="Unknown patient")
        return human_to_document(patient)

    return app
