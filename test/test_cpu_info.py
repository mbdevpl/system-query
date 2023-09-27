"""Tests for cpu_info module."""

import unittest
import unittest.mock

from system_query.available_features import CPU
import system_query.cpu_info
from system_query.cpu_info import query_cpu_clock, query_cpu_cores, _get_cache_size


class Tests(unittest.TestCase):

    @unittest.skipIf(not CPU, 'skipping CPU cache query')
    def test_cpu_cache_size(self):
        info = _get_cache_size(1, {'l1_cache_size': '512'})
        self.assertIsInstance(info, int)
        self.assertEqual(info, 512 * 1024)

    @unittest.skipIf(not CPU, 'skipping CPU cache query')
    def test_cpu_cache_size_with_units(self):
        info = _get_cache_size(1, {'l1_cache_size': '512 kB'})
        self.assertIsInstance(info, int)
        self.assertEqual(info, 512 * 1000)
        info = _get_cache_size(1, {'l1_cache_size': '512 KB'})
        self.assertIsInstance(info, int)
        self.assertEqual(info, 512 * 1024)
        info = _get_cache_size(1, {'l1_cache_size': '512 KiB'})
        self.assertIsInstance(info, int)
        self.assertEqual(info, 512 * 1024)
        info = _get_cache_size(1, {'l1_cache_size': '2 MB'})
        self.assertIsInstance(info, int)
        self.assertEqual(info, 2 * 1024 ** 2)
        info = _get_cache_size(1, {'l1_cache_size': '4 MiB'})
        self.assertIsInstance(info, int)
        self.assertEqual(info, 4 * 1024 ** 2)

    @unittest.skipIf(not CPU, 'skipping CPU cache query')
    def test_cpu_cache_size_with_units_and_instances(self):
        info = _get_cache_size(1, {'l1_cache_size': '192 KiB (6 instances)'})
        self.assertIsInstance(info, int)
        self.assertEqual(info, 192 * 1024)

    @unittest.skipIf(not CPU, 'skipping CPU cache query')
    def test_query_cpu_clock_unsupported(self):
        with unittest.mock.patch.object(system_query.cpu_info, 'CPU_CLOCK', False):
            self.assertEqual(query_cpu_clock(), (None, None, None))

    @unittest.skipIf(not CPU, 'skipping CPU cache query')
    def test_query_cpu_cores_unsupported(self):
        with unittest.mock.patch.object(system_query.cpu_info, 'CPU_CORES', False):
            self.assertEqual(query_cpu_cores(), (None, None))
