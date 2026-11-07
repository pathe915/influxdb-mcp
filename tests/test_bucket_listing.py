"""Regression tests for bucket listing with organization names and IDs."""

from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from influxdb_mcp.influxdb_client import InfluxDBManager


@pytest.mark.parametrize(
    ("org", "expected_filter"),
    [
        ("bef512adcb3254dc", {"org_id": "bef512adcb3254dc"}),
        ("homey-org", {"org": "homey-org"}),
    ],
)
def test_list_buckets_uses_correct_organization_filter(org, expected_filter):
    manager = InfluxDBManager(SimpleNamespace(org=org))
    bucket = SimpleNamespace(
        name="Homey",
        type="user",
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        updated_at=None,
    )
    manager._buckets_api = Mock()
    manager._buckets_api.find_buckets_iter.return_value = [bucket]

    result = manager.list_buckets()

    manager._buckets_api.find_buckets_iter.assert_called_once_with(**expected_filter)
    assert result == [
        {
            "name": "Homey",
            "type": "user",
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": None,
        }
    ]


def test_list_buckets_handles_empty_result():
    manager = InfluxDBManager(SimpleNamespace(org="bef512adcb3254dc"))
    manager._buckets_api = Mock()
    manager._buckets_api.find_buckets_iter.return_value = []

    assert manager.list_buckets() == []
