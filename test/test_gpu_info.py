"""Tests for gpu_info module."""

import collections.abc
import unittest

from system_query.gpu_info import query_gpus


class Tests(unittest.TestCase):

    def test_query_gpus(self):
        info = query_gpus()
        self.assertIsInstance(info, collections.abc.Sequence)
