"""Software system test for the HTML results report. Verifies: SSS009"""

import pytest


def test_html_report_path_and_metadata(
    pytestconfig: pytest.Config, metadata: dict[str, str]
) -> None:
    """The run is configured to write the self-contained HTML report.

    Verifies: SSS009
    """
    html_path = str(pytestconfig.getoption("htmlpath"))
    assert html_path.endswith("docs/pytest-report.html")
    assert pytestconfig.getoption("self_contained_html") is True
    assert metadata["Software version"] == "0.1.0"
    assert metadata["Device configuration"] == "mock patient monitor 0.1.0"
    assert "pytest" in metadata["Test tools"]
    assert metadata["Operator"]
