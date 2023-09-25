"""Tests for all_info module."""

import collections.abc
import platform
import unittest

from system_query.all_info import query_all


class IntegrationChecks(unittest.TestCase):
    """Check all info modules."""

    def query_all_and_check(self, sudo: bool):
        """Check that query results contain expected entries."""
        info = query_all(sudo=sudo)
        self.assertIsInstance(info, collections.abc.Mapping)
        self.assertGreater(len(info), 1)
        self.assertIn('host', info)
        self.assertIn('os', info)
        self.assertIn('cpu', info)
        self.assertIn('ram', info)
        if not sudo:
            return
        min_length = 1 if platform.system() == 'Linux' else 0
        ram_banks = info.get('ram', {}).get('banks', [])
        self.assertGreaterEqual(len(ram_banks), min_length)
        for ram_bank in ram_banks:
            self.assertIsInstance(ram_bank, dict)


class Tests(IntegrationChecks):

    def test_query_all(self):
        self.query_all_and_check(False)
