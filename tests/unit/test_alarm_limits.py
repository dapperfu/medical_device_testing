"""Unit tests for alarm-limit command acceptance.

Verifies: SSS002, SSS007
"""

import pytest

from medical_device_testing.device.alarm_limits import (
    AlarmLimits,
    LimitRejected,
    accept_limits,
)


def test_default_profiles_are_accepted() -> None:
    """Adult and pediatric defaults are inside the command range.

    Verifies: SSS002, SSS007
    """
    accept_limits(AlarmLimits.adult_defaults())
    accept_limits(AlarmLimits.pediatric_defaults())
    assert AlarmLimits.for_age(18) == AlarmLimits.adult_defaults()
    assert AlarmLimits.for_age(17) == AlarmLimits.pediatric_defaults()


def test_rejects_spo2_above_100() -> None:
    """SpO2 low limit 101 is rejected. Verifies: SSS007"""
    rejected = AlarmLimits(50, 120, 101, 160, 100, 35.0, 38.0)
    with pytest.raises(LimitRejected):
        accept_limits(rejected)


def test_rejects_heart_rate_high_not_above_low() -> None:
    """Heart-rate high limit must be greater than the low limit. Verifies: SSS007"""
    rejected = AlarmLimits(80, 80, 90, 160, 100, 35.0, 38.0)
    with pytest.raises(LimitRejected):
        accept_limits(rejected)


def test_rejects_temperature_high_not_above_low() -> None:
    """Temperature high limit must be greater than the low limit. Verifies: SSS007"""
    rejected = AlarmLimits(50, 120, 90, 160, 100, 37.0, 36.0)
    with pytest.raises(LimitRejected):
        accept_limits(rejected)
