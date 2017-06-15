"""Tests of packaging."""

import contextlib
import io
import runpy
import sys
import unittest


class Tests(unittest.TestCase):

    def run_setup(self, *args):
        sys.argv = ['setup.py'] + list(args)
        runpy.run_module('setup', run_name='__main__')

    @unittest.skip('failing in this context')
    def test_bdist(self):
        _ = io.StringIO()
        with contextlib.redirect_stdout(_):
            self.run_setup('bdist')

    def test_bdist_wheel(self):
        _ = io.StringIO()
        with contextlib.redirect_stdout(_):
            self.run_setup('bdist_wheel')

    def test_sdist(self):
        _ = io.StringIO()
        with contextlib.redirect_stdout(_):
            self.run_setup('sdist', '--formats=gztar,zip')
