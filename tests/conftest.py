"""Pytest plugins and HTML report metadata. Verifies: SSS008, SSS009"""

import getpass
from importlib.metadata import version

pytest_plugins = [
    "tests.fixtures.healthy_adult",
    "tests.fixtures.tachycardic_adult",
    "tests.fixtures.hypoxic_adult",
    "tests.fixtures.hypertensive_adult",
    "tests.fixtures.pediatric_patient",
    "tests.fixtures.sensor_fault_patient",
    "tests.fixtures.patient_monitor",
]


def pytest_metadata(metadata: dict[str, str]) -> None:
    """Record the software version, tools, and the person who ran the test.

    Verifies: SSS009
    """
    metadata["Software version"] = version("medical_device_testing")
    metadata["Device configuration"] = "mock patient monitor 0.1.0"
    metadata["Test tools"] = "pytest, pytest-html"
    metadata["Operator"] = getpass.getuser()
