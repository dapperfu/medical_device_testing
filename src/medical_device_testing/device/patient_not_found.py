"""Shared failure when a remote patient lookup does not return a patient.

Implements: SSS011, SSS013
"""


class PatientNotFound(Exception):
    """A remote lookup did not produce a patient. Implements: SSS011, SSS013"""
