"""Command-line interface of system_query."""

import argparse
import pathlib
import sys

from ._version import VERSION
from .query import query_and_export


def main(args=None, namespace=None):
    """Parse command line arguments and execute query_and_export() function according to them."""

    program_name = 'system_query'
    parser = argparse.ArgumentParser(
        prog=program_name, description='''Comprehensive and concise system information tool.
        Query a given hardware and/or softawre scope of your system and get results in human-
        and machine-readable formats.''',
        epilog='''Copyright 2017-2018 by the contributors, Apache License 2.0,
        https://github.com/mbdevpl/system-query''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=True)
    parser.add_argument(
        '-s', '--scope', type=str, default='all', choices=['all', 'cpu', 'gpu', 'ram'],
        help='''Scope of the query''')
    parser.add_argument(
        '-f', '--format', type=str, default='raw', choices=['raw', 'json'],
        help='''Format of the results of the query.''')
    parser.add_argument(
        '-t', '--target', type=str, default='stdout',
        help='''File path where to write the results of the query. Special values: "stdout"
        and "stderr" to write to stdout and stderr, respectively.''')
    parser.add_argument(
        '--version', action='version',
        version='{} {},\nPython {}'.format(program_name, VERSION, sys.version))

    args = parser.parse_args(args=args, namespace=namespace)
    target = {
        'stdout': sys.stdout,
        'stderr': sys.stderr
        }.get(args.target, pathlib.Path(args.target))
    query_and_export(query_scope=args.scope, export_format=args.format, export_target=target)
