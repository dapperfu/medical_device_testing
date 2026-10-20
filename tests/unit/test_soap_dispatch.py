"""Unit tests for SOAP request dispatch. Verifies: SSS010, SSS011"""

from medical_device_testing.device.soap_patient_service import _dispatch
from medical_device_testing.humans.healthy_adult import HealthyAdult
from medical_device_testing.humans.sensor_fault_patient import SensorFaultPatient


def _request(patient_id: str) -> bytes:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
        "<soap:Body>"
        '<GetPatient xmlns="urn:medical-device-testing:patient">'
        f"<patientId>{patient_id}</patientId>"
        "</GetPatient></soap:Body></soap:Envelope>"
    ).encode()


def test_dispatch_returns_registered_patient() -> None:
    """GetPatient returns the registered vital fields. Verifies: TD028, SSS010"""
    patient = HealthyAdult()
    payload = _dispatch(_request(patient.patient_id), {patient.patient_id: patient})
    text = payload.decode("utf-8")
    assert "soap:Fault" not in text
    assert "<patientId>healthy-adult</patientId>" in text
    assert "<heartRateBpm>72</heartRateBpm>" in text
    assert "<sensorValid>true</sensorValid>" in text


def test_dispatch_omits_invalid_sensor_vitals() -> None:
    """An invalid sensor is reported without numeric vitals. Verifies: TD029, SSS010"""
    patient = SensorFaultPatient()
    payload = _dispatch(_request(patient.patient_id), {patient.patient_id: patient})
    text = payload.decode("utf-8")
    assert "<sensorValid>false</sensorValid>" in text
    assert "heartRateBpm" not in text


def test_dispatch_unknown_patient_is_a_fault() -> None:
    """An unknown id returns a SOAP fault. Verifies: TD030, SSS011"""
    payload = _dispatch(_request("missing"), {})
    assert b"soap:Fault" in payload
    assert b"Unknown patient" in payload


def test_dispatch_malformed_xml_is_a_fault() -> None:
    """A body that is not XML returns a SOAP fault. Verifies: TD031, SSS011"""
    payload = _dispatch(b"not-xml", {})
    assert b"Malformed SOAP request" in payload
