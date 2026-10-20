"""Client for the ReadyAPI patient resource.

Implements: SSS012, SSS013, IRS006
"""

from typing import Protocol

from medical_device_testing.device.patient_not_found import PatientNotFound
from medical_device_testing.device.readyapi_patient_service import human_from_document
from medical_device_testing.humans.human import Human


class PatientResponse(Protocol):
    """Subset of the ReadyAPI test client response. Implements: IRS006"""

    status_code: int

    def json(self) -> dict[str, object]:
        """Return the JSON body."""


class PatientClient(Protocol):
    """GET client used to reach the ReadyAPI app. Implements: IRS006"""

    def get(self, path: str) -> PatientResponse:
        """Request one path."""


class ReadyApiPatientDevice:
    """Third mock device. It obtains the patient from ReadyAPI. Implements: SSS012"""

    def __init__(self, client: PatientClient) -> None:
        self._client = client

    def get_patient(self, patient_id: str) -> Human:
        """Return the Human from GET /patients/{id}. Implements: SSS012, SSS013"""
        response = self._client.get(f"/patients/{patient_id}")
        if response.status_code == 404:
            raise PatientNotFound(patient_id)
        if response.status_code != 200:
            raise PatientNotFound(patient_id)
        return human_from_document(response.json())
