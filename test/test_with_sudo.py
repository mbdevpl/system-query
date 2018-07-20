"""Tests for functionality that requires administrative access."""

import collections.abc
import getpass
import unittest

from system_query.all_info import query_all


@unittest.skipUnless(getpass.getuser() == 'root', 'skipping tests that require sudo')
class Tests(unittest.TestCase):

    def test_query_all_sudo(self):
        info = query_all(sudo=True)
        self.assertIsInstance(info, collections.abc.Mapping)
        self.assertGreater(len(info), 1)
        self.assertIn('host', info)
        self.assertIn('os', info)
        self.assertIn('cpu', info)
        self.assertIn('ram', info)
        self.assertGreaterEqual(len(info.get('ram', {}).get('banks', [])), 1)
