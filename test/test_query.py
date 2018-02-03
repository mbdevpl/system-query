"""Tests for query and export utility function."""

import sys
import logging
import unittest

from system_query.query import query_and_export

_LOG = logging.getLogger(__name__)


class Tests(unittest.TestCase):

    def test_unsupported_scope(self):
        with self.assertRaises(NotImplementedError):
            query_and_export('host', 'raw', sys.stdout)
        with self.assertRaises(NotImplementedError):
            query_and_export('os', 'raw', sys.stdout)
        with self.assertRaises(NotImplementedError):
            query_and_export('swap', 'raw', sys.stdout)

    def test_unsupported_format(self):
        with self.assertRaises(NotImplementedError):
            query_and_export('all', 'xml', sys.stdout)
        with self.assertRaises(NotImplementedError):
            query_and_export('all', 'yaml', sys.stdout)

    def test_unsupported_target(self):
        with self.assertRaises(NotImplementedError):
            query_and_export('all', 'raw', 12345)
        with self.assertRaises(NotImplementedError):
            query_and_export('all', 'json', 12345)
