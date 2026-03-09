"""Tests for CLI argument parsing and helpers."""

import pytest

from src.cli.main import _parse_duration


class TestParseDuration:
    def test_days(self):
        assert _parse_duration("90d") == 90

    def test_months(self):
        assert _parse_duration("6m") == 180

    def test_years(self):
        assert _parse_duration("1y") == 365

    def test_uppercase(self):
        assert _parse_duration("30D") == 30

    def test_with_spaces(self):
        assert _parse_duration(" 7d ") == 7

    def test_invalid_exits(self):
        with pytest.raises(SystemExit):
            _parse_duration("abc")

    def test_no_unit_exits(self):
        with pytest.raises(SystemExit):
            _parse_duration("90")

    def test_invalid_unit_exits(self):
        with pytest.raises(SystemExit):
            _parse_duration("90w")
