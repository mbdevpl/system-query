"""Tests for using system_query from command line."""

import ast
import contextlib
import io
import itertools
import json
import logging
import os
import tempfile
import unittest

from .test_setup import run_module

_LOG = logging.getLogger(__name__)


class Tests(unittest.TestCase):

    def test_not_as_main(self):
        sio = io.StringIO()
        with contextlib.redirect_stdout(sio):
            run_module('system_query', run_name=None)
        self.assertEqual(sio.getvalue(), '')

    def test_help(self):
        sio = io.StringIO()
        with contextlib.redirect_stdout(sio):
            with self.assertRaises(SystemExit):
                run_module('system_query', '-h')
        _LOG.info('%s', sio.getvalue())

    def test_default_format(self):
        sio = io.StringIO()
        with contextlib.redirect_stdout(sio):
            run_module('system_query')
        self.assertIsInstance(ast.literal_eval(sio.getvalue()), dict)

        for args in itertools.product(['--scope'], ['all', 'cpu', 'gpu', 'ram']):
            sio = io.StringIO()
            with contextlib.redirect_stdout(sio):
                run_module('system_query', *args)
            self.assertIsInstance(ast.literal_eval(sio.getvalue()), (list, dict), msg=args)

    def test_json(self):
        sio = io.StringIO()
        with contextlib.redirect_stdout(sio):
            run_module('system_query', '--format', 'json')
        json_data = json.loads(sio.getvalue())
        self.assertIsNotNone(json_data)

        for args in itertools.product(['--scope'], ['all', 'cpu', 'gpu', 'ram']):
            sio = io.StringIO()
            with contextlib.redirect_stdout(sio):
                run_module('system_query', '--format', 'json', *args)
            json_data = json.loads(sio.getvalue())
            self.assertIsNotNone(json_data, msg=args)

    def test_raw(self):
        sio = io.StringIO()
        with contextlib.redirect_stdout(sio):
            run_module('system_query', '--format', 'raw')
        self.assertIsInstance(ast.literal_eval(sio.getvalue()), dict)

    def test_file(self):
        loaders = {'raw': ast.literal_eval, 'json': json.loads}
        for fmt in ('raw', 'json'):
            with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
                tmpfile_name = tmpfile.name
            run_module('system_query', '--format', fmt, '--target', tmpfile_name)
            with open(tmpfile_name) as tmpfile:
                data = loaders[fmt](tmpfile.read())
                self.assertIsInstance(data, dict)
                self.assertGreater(len(data), 0)
            os.remove(tmpfile_name)
