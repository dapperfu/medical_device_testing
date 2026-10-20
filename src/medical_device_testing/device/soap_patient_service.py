"""Local SOAP 1.1 stub that serves registered Human records.

Implements: SSS010, SSS011, IRS005
"""

from collections.abc import Mapping
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from xml.etree import ElementTree
from xml.sax.saxutils import escape

from medical_device_testing.humans.human import Human

SOAP_ENV = "http://schemas.xmlsoap.org/soap/envelope/"
PATIENT_NS = "urn:medical-device-testing:patient"
_NS = {"soap": SOAP_ENV, "pat": PATIENT_NS}


def human_to_fields(patient: Human) -> dict[str, str]:
    """Serialize a Human into SOAP response fields. Implements: SSS010"""
    fields = {
        "patientId": patient.patient_id,
        "ageYears": str(patient.age_years),
        "sensorValid": "true" if patient.sensor_valid else "false",
    }
    optional = {
        "heartRateBpm": patient.heart_rate_bpm,
        "spo2Percent": patient.spo2_percent,
        "systolicMmhg": patient.systolic_mmhg,
        "diastolicMmhg": patient.diastolic_mmhg,
        "temperatureC": patient.temperature_c,
    }
    for name, value in optional.items():
        if value is not None:
            fields[name] = str(value)
    return fields


def human_from_fields(fields: Mapping[str, str]) -> Human:
    """Build a Human from SOAP or JSON fields. Implements: SSS010, SSS012"""

    def optional_int(name: str) -> int | None:
        raw = fields.get(name)
        if raw is None or raw == "":
            return None
        return int(raw)

    def optional_float(name: str) -> float | None:
        raw = fields.get(name)
        if raw is None or raw == "":
            return None
        return float(raw)

    sensor = fields.get("sensorValid", "true").lower()
    return Human(
        patient_id=fields["patientId"],
        age_years=int(fields["ageYears"]),
        heart_rate_bpm=optional_int("heartRateBpm"),
        spo2_percent=optional_int("spo2Percent"),
        systolic_mmhg=optional_int("systolicMmhg"),
        diastolic_mmhg=optional_int("diastolicMmhg"),
        temperature_c=optional_float("temperatureC"),
        sensor_valid=sensor == "true",
    )


def _soap_response(body_xml: str) -> bytes:
    envelope = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<soap:Envelope xmlns:soap="{SOAP_ENV}">'
        f"<soap:Body>{body_xml}</soap:Body>"
        "</soap:Envelope>"
    )
    return envelope.encode("utf-8")


def _fault(message: str) -> bytes:
    body = (
        "<soap:Fault>"
        "<faultcode>soap:Client</faultcode>"
        f"<faultstring>{message}</faultstring>"
        "</soap:Fault>"
    )
    return _soap_response(body)


def _patient_xml(patient: Human) -> str:
    fields = human_to_fields(patient)
    inner = "".join(
        f"<{name}>{escape(value)}</{name}>" for name, value in fields.items()
    )
    return f'<GetPatientResponse xmlns="{PATIENT_NS}">{inner}</GetPatientResponse>'


class SoapPatientService:
    """SOAP 1.1 GetPatient endpoint bound to 127.0.0.1. Implements: SSS010, SSS011"""

    def __init__(self) -> None:
        self._patients: dict[str, Human] = {}
        handler = self._handler_type()
        self._httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self._thread = Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()

    def register(self, patient: Human) -> None:
        """Store a patient the stub may return. Implements: SSS010"""
        self._patients[patient.patient_id] = patient

    @property
    def endpoint(self) -> str:
        """Return the local SOAP URL. Implements: IRS005"""
        _host, port = self._httpd.server_address
        return f"http://127.0.0.1:{port}/patient"

    def close(self) -> None:
        """Stop the stub. Implements: SSS010"""
        self._httpd.shutdown()
        self._httpd.server_close()
        self._thread.join(timeout=2)

    def _handler_type(self) -> type[BaseHTTPRequestHandler]:
        patients = self._patients

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802
                length = int(self.headers.get("Content-Length", "0"))
                raw = self.rfile.read(length)
                payload = _dispatch(raw, patients)
                status = 500 if b"soap:Fault" in payload else 200
                self.send_response(status)
                self.send_header("Content-Type", "text/xml; charset=utf-8")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, _format: str, *_args: object) -> None:
                return

        return Handler


def _dispatch(raw: bytes, patients: Mapping[str, Human]) -> bytes:
    try:
        root = ElementTree.fromstring(raw)
    except ElementTree.ParseError:
        return _fault("Malformed SOAP request")
    patient_id = root.findtext(".//pat:patientId", namespaces=_NS)
    if patient_id is None:
        patient_id = root.findtext(".//patientId")
    if not patient_id or patient_id not in patients:
        return _fault("Unknown patient")
    return _soap_response(_patient_xml(patients[patient_id]))
