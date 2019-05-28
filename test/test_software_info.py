"""Tests for software_info module."""

import collections.abc
import unittest

from system_query.software_info import query_software


class Tests(unittest.TestCase):

    def test_query_software(self):
        info = query_software()
        self.assertIsInstance(info, collections.abc.Mapping)
