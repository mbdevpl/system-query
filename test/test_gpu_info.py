"""Tests for gpu_info module."""

import collections.abc
import unittest

from system_query.gpu_info import query_gpus, calculate_cuda_cores


class Tests(unittest.TestCase):

    def test_query_gpus(self):
        info = query_gpus()
        self.assertIsInstance(info, collections.abc.Sequence)

    def test_calculate_cuda_cores(self):
        for multiprocessors in (1, 2, 4, 128, 1024):
            self.assertEqual(calculate_cuda_cores((1, 0), multiprocessors), None)
            self.assertEqual(calculate_cuda_cores((2, 0), multiprocessors), 32 * multiprocessors)
            self.assertEqual(calculate_cuda_cores((2, 1), multiprocessors), 48 * multiprocessors)
            self.assertEqual(calculate_cuda_cores((2, 2), multiprocessors), 32 * multiprocessors)
            self.assertEqual(calculate_cuda_cores((5, 0), multiprocessors), 128 * multiprocessors)
            self.assertEqual(calculate_cuda_cores((5, 2), multiprocessors), 128 * multiprocessors)
            self.assertEqual(calculate_cuda_cores((5, 3), multiprocessors), 128 * multiprocessors)
            self.assertEqual(calculate_cuda_cores((6, 0), multiprocessors), 64 * multiprocessors)
            self.assertEqual(calculate_cuda_cores((6, 1), multiprocessors), 128 * multiprocessors)
            self.assertEqual(calculate_cuda_cores((6, 2), multiprocessors), None)
            self.assertEqual(calculate_cuda_cores((8, 0), multiprocessors), None)
            self.assertEqual(calculate_cuda_cores((9, 0), multiprocessors), None)
