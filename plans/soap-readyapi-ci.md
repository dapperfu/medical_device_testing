---
name: SOAP ReadyAPI CI
overview: Add a SOAP client device backed by a local SOAP 1.1 stub, a third device that reads the patient from a ReadyAPI 0.112.0 service, and a GitHub Actions workflow that runs pytest and archives the HTML report.
todos:
  - id: save-plan
    content: Save this plan to plans/soap-readyapi-ci.md
    status: completed
  - id: requirements
    content: Add SRS006-SRS007, SSS010-SSS013, SDD, IRS, TP, and TD entries and regenerate docs/html
    status: pending
  - id: soap-device
    content: Implement SoapPatientService and SoapPatientDevice with fixtures and tests
    status: completed
  - id: readyapi-device
    content: Pin readyapi 0.112.0 and implement ReadyApiPatientService and ReadyApiPatientDevice with fixtures and tests
    status: completed
  - id: github-actions
    content: Add the GitHub Actions workflow that runs make test and archives docs/pytest-report.html
    status: pending
isProject: false
---

# SOAP device, ReadyAPI device, and GitHub Actions

The existing `PatientMonitor` stays the in-process mock. Class C, confirmed on 2026-10-20, still applies to the new software items. No segregation is claimed. This remains a mock, not a conformity claim. `SSS006` and `SSS007` are unchanged.

You chose a local SOAP 1.1 stub plus a client device, and the Python package `readyapi==0.112.0` (the Starlette/Pydantic framework, not SmartBear ReadyAPI).

## SOAP device

New units under [`src/medical_device_testing/device/`](src/medical_device_testing/device/):

- `SoapPatientService`: stdlib `http.server` on `127.0.0.1` and an ephemeral port. SOAP 1.1 `GetPatient` takes `patientId` and returns the registered `Human` fields (`ageYears`, five vitals, `sensorValid`). Unknown id or malformed XML returns a SOAP fault. No new SOAP library, so this stack is not new SOUP.
- `SoapPatientDevice`: POSTs that envelope and returns a `Human`. A fault or unknown patient raises `PatientNotFound` and does not return a patient.

Pytest fixture `soap_patient_service` registers the existing patient fixtures and shuts the server down after the test. `soap_patient_device` is function scoped.

## ReadyAPI device

`readyapi==0.112.0` becomes a runtime dependency in [`pyproject.toml`](pyproject.toml) and is locked in `uv.lock`. It is SOUP (KhulnaSoft; Starlette and Pydantic come with it). [`requirements/sdp/SDP.sdoc`](requirements/sdp/SDP.sdoc) `SDP004` will name that version. Published-anomaly review is still not done, and this mock is not released device software.

- `ReadyApiPatientService`: `ReadyAPI()` app, `GET /patients/{patient_id}`, JSON body with the same fields as `Human`. Missing id returns 404.
- `ReadyApiPatientDevice`: calls that route and returns a `Human`, or raises `PatientNotFound` on 404.

Tests use the app's ASGI test client when `readyapi` 0.112.0 exports one; otherwise Starlette's `TestClient`. No separate uvicorn process.

## Requirements to add

Parent links stay SRS to SSS to design, interface, and test descriptions. Approving this plan approves these statements.

- `SRS006`: The SOAP patient device shall obtain identity, age, vitals, and sensor validity from a SOAP 1.1 `GetPatient` response.
- `SRS007`: The ReadyAPI patient device shall obtain those same fields from the ReadyAPI patient resource.
- `SSS010` (parent `SRS006`): `SoapPatientDevice` shall return a `Human` matching the `GetPatient` body, including `sensor_valid` false when the body says the sensor is invalid.
- `SSS011` (parent `SRS006`): A SOAP fault or unknown patient shall not produce a `Human`.
- `SSS012` (parent `SRS007`): `ReadyApiPatientDevice` shall return a `Human` matching the JSON patient resource.
- `SSS013` (parent `SRS007`): An unknown ReadyAPI patient shall not produce a `Human`.
- `SDD006` / `IRS005`: SOAP service and `GetPatient` client.
- `SDD007` / `IRS006`: ReadyAPI service and `GET /patients/{patient_id}`.
- `TP005` and `TD028` onward: one description per new test, parent-linked to `SSS010` through `SSS013`.

One integration test fetches `SensorFaultPatient` over each transport and attaches that `Human` to the existing `PatientMonitor`, so `SSS006` still applies after remote acquisition.

## GitHub Actions

Add [`.github/workflows/pytest.yml`](.github/workflows/pytest.yml). On push and pull request, `ubuntu-latest` checks out the repo, installs uv, runs `make test`, and uploads `docs/pytest-report.html` with `actions/upload-artifact`. The upload uses `if: always()` so a failed run still archives the report. The workflow does not install SmartBear ReadyAPI.

[`README.md`](README.md) will name both devices and the artifact. [`Makefile`](Makefile) `test` target stays the CI command.
