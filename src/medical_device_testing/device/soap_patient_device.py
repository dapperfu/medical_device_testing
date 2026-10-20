"""SOAP 1.1 client that reads a patient from SoapPatientService.

Implements: SSS010, SSS011, IRS005
"""

from urllib.error import HTTPError
from urllib.request import Request, urlopen
from xml.etree import ElementTree
from xml.sax.saxutils import escape

from medical_device_testing.device.patient_not_found import PatientNotFound
from medical_device_testing.device.soap_patient_service import (
    PATIENT_NS,
    SOAP_ENV,
    human_from_fields,
)
from medical_device_testing.humans.human import Human

_NS = {"soap": SOAP_ENV, "pat": PATIENT_NS}


class SoapPatientDevice:
    """Second mock device. It obtains the patient over SOAP. Implements: SSS010"""

    def __init__(self, endpoint: str) -> None:
        self._endpoint = endpoint

    def get_patient(self, patient_id: str) -> Human:
        """Return the Human from GetPatient. Implements: SSS010, SSS011"""
        body = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            f'<soap:Envelope xmlns:soap="{SOAP_ENV}">'
            "<soap:Body>"
            f'<GetPatient xmlns="{PATIENT_NS}">'
            f"<patientId>{escape(patient_id)}</patientId>"
            "</GetPatient>"
            "</soap:Body>"
            "</soap:Envelope>"
        )
        request = Request(
            self._endpoint,
            data=body.encode("utf-8"),
            headers={"Content-Type": "text/xml; charset=utf-8"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=5) as response:  # noqa: S310
                payload = response.read()
        except HTTPError as error:
            payload = error.read()
            if b"Fault" in payload:
                raise PatientNotFound(patient_id) from error
            raise
        return _human_from_soap(payload)


def _human_from_soap(payload: bytes) -> Human:
    try:
        root = ElementTree.fromstring(payload)
    except ElementTree.ParseError as error:
        raise PatientNotFound("malformed response") from error
    if root.find(".//soap:Fault", _NS) is not None:
        raise PatientNotFound("soap fault")
    response = root.find(".//pat:GetPatientResponse", _NS)
    if response is None:
        raise PatientNotFound("missing response")
    fields = {child.tag.rpartition("}")[2]: (child.text or "") for child in response}
    if "patientId" not in fields or "ageYears" not in fields:
        raise PatientNotFound("incomplete response")
    return human_from_fields(fields)
