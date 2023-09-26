"""Tests for available_features module."""

import unittest

from system_query.available_features import GPU, HDD
from system_query import query_gpus, query_hdds


class Tests(unittest.TestCase):

    @unittest.skipUnless(GPU, 'querying GPUs is not supported')
    def test_gpus(self):
        self.assertGreaterEqual(len(query_gpus()), 1)

    @unittest.skipUnless(HDD, 'querying HDDs is not supported')
    def test_hdds(self):
        self.assertGreaterEqual(len(query_hdds()), 1)
