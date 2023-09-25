"""Initialization of tests for system_query package."""

import logging

from system_query.__main__ import Logging


class TestsLogging(Logging):
    """Test logging configuration."""

    level_package = logging.DEBUG


TestsLogging.configure()
