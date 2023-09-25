"""Tests for available_features module."""

import unittest

from system_query.available_features import HDD
from system_query import query_hdds


class Tests(unittest.TestCase):

    @unittest.skipUnless(HDD, 'querying HDDs is not supported')
    def test_hdds(self):
        self.assertGreaterEqual(len(query_hdds()), 1)
