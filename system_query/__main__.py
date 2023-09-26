"""Entry point of the command-line interface of system_query package."""

import logging

import boilerplates.logging

from .main import main


class Logging(boilerplates.logging.Logging):
    """Logging configuration."""

    packages = ['system_query']
    level_global = logging.WARNING


if __name__ == '__main__':
    Logging.configure()
    main()
