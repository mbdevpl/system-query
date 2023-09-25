"""Tests for functionality that requires administrative access."""

import getpass
import unittest

from .test_all_info import IntegrationChecks


@unittest.skipUnless(getpass.getuser() == 'root', 'skipping tests that require sudo')
class Tests(IntegrationChecks):

    def test_query_all_sudo(self):
        self.query_all_and_check(True)
