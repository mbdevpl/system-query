"""Tests for available_features module."""

import unittest

from system_query.available_features import CPU, GPU, HDD, SWAP
from system_query import query_cpu, query_gpus, query_hdds, query_swap


class Tests(unittest.TestCase):

    @unittest.skipUnless(CPU, 'querying CPU is not supported')
    def test_cpu(self):
        self.assertGreaterEqual(len(query_cpu()), 1)

    @unittest.skipUnless(GPU, 'querying GPUs is not supported')
    def test_gpus(self):
        self.assertGreaterEqual(len(query_gpus()), 1)

    @unittest.skipUnless(HDD, 'querying HDDs is not supported')
    def test_hdds(self):
        self.assertGreaterEqual(len(query_hdds()), 1)

    @unittest.skipUnless(SWAP, 'querying swap is not supported')
    def test_swap(self):
        self.assertGreaterEqual(len(query_swap()), 1)
