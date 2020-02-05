"""Initialization of tests of system_query package."""

import logging
import os

import colorlog

_HANDLER = logging.StreamHandler()
_HANDLER.setFormatter(colorlog.ColoredFormatter(
    '{name} [{log_color}{levelname}{reset}] {message}', style='{'))

logging.basicConfig(level=logging.DEBUG, handlers=[_HANDLER])
logging.getLogger().setLevel(logging.WARNING)
logging.getLogger('system_query').setLevel(
    getattr(logging, os.environ.get('LOGGING_LEVEL', 'debug').upper()))
logging.getLogger('test').setLevel(logging.DEBUG)
