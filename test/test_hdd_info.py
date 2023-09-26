"""Tests for hdd_info module."""

import unittest

from system_query.available_features import HDD
from system_query.hdd_info import query_hdds


@unittest.skipIf(not HDD, 'skipping HDD query')
class Tests(unittest.TestCase):

    def test_query_hdds(self):
        info = query_hdds()
        self.assertIsInstance(info, dict)
        self.assertGreaterEqual(len(info), 1)
        self.assertTrue(next(iter(info)).startswith('/dev'))
