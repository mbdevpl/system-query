"""Tests for using system_query from command line."""

import ast
import contextlib
import io
import json
import logging
import runpy
import sys
import unittest

_LOG = logging.getLogger(__name__)


class Tests(unittest.TestCase):

    def run_module(self, module, *args, run_name: str = '__main__'):
        sys.argv = [module] + list(args)
        runpy.run_module(module, run_name=run_name)

    def test_not_as_main(self):
        self.run_module('system_query', run_name=None)

    def test_help(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            with self.assertRaises(SystemExit):
                self.run_module('system_query', '-h')
        _LOG.info('%s', f.getvalue())

    def test_default_format(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.run_module('system_query')
        self.assertIsInstance(ast.literal_eval(f.getvalue()), dict)

    def test_json(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.run_module('system_query', '--format', 'json')
        json_data = json.loads(f.getvalue())
        self.assertIsNotNone(json_data)

    def test_raw(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.run_module('system_query', '--format', 'raw')
        self.assertIsInstance(ast.literal_eval(f.getvalue()), dict)
