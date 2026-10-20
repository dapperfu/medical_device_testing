"""StrictDoc project configuration for medical_device_testing."""

from strictdoc.core.project_config import ProjectConfig


def create_config() -> ProjectConfig:
    """Return the project config used by export and the web server."""
    return ProjectConfig(
        project_title="medical_device_testing",
        dir_for_sdoc_cache=".strictdoc_cache",
    )
