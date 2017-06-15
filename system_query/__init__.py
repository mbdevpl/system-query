"""This is __init__ module of system_query package.

It consists of utility functions for exporting system information to various formats
and the main() function.
"""

import argparse
import json
import pathlib
import pprint
import sys
import typing as t

from .all_info import query_all
from .cpu_info import query_cpu
from .gpu_info import query_gpus
#from .host_info import query_host
#from .os_info import query_os
from .ram_info import query_ram
#from .swap_info import query_swap
from ._version import VERSION

__version__ = VERSION

JSON_INDENT = 2

ENSURE_ASCII = False


def query_and_export(query_scope: str, export_format: str, export_target: t.Any, **kwargs):
    """Query the given scope of the system and export results in a given format to a given target.

    Currently implemented values are:

    - query_scope: all, cpu, gpu, ram, swap.
    - export_format: json, raw.
    - export_target: sys.stdout, sys.stderr, path.
    """

    if query_scope == 'all':
        info = query_all(**kwargs)
    elif query_scope == 'cpu':
        info = query_cpu(**kwargs)
    elif query_scope == 'gpu':
        info = query_gpus(**kwargs)
    elif query_scope == 'ram':
        info = query_ram(**kwargs)
    else:
        raise NotImplementedError('scope={}'.format(query_scope))

    if export_format == 'json':
        if export_target in (sys.stdout, sys.stderr):
            json_str = json.dumps(info, indent=JSON_INDENT, ensure_ascii=ENSURE_ASCII)
            print(json_str, file=export_target)
        elif isinstance(export_target, pathlib.Path):
            with open(export_target, 'w', encoding='utf-8') as json_file:
                json.dump(info, json_file, indent=JSON_INDENT, ensure_ascii=ENSURE_ASCII)
        else:
            raise NotImplementedError('format={} target={}'.format(export_format, export_target))
    elif export_format == 'raw':
        if export_target in (sys.stdout, sys.stderr):
            pprint.pprint(info, stream=export_target)
        elif isinstance(export_target, pathlib.Path):
            with open(export_target, 'a', encoding='utf-8') as text_file:
                text_file.write(str(info))
        else:
            raise NotImplementedError('format={} target={}'.format(export_format, export_target))
    else:
        raise NotImplementedError('format={} target={}'.format(export_format, export_target))


def main(args=None, namespace=None):
    """Parse command line arguments and execute query_and_export() function according to them."""

    program_name = 'system_query'
    parser = argparse.ArgumentParser(
        prog=program_name, description='''Comprehensive and concise system information tool.
        Query a given hardware and/or softawre scope of your system and get results in human-
        and machine-readable formats.''',
        epilog='''Copyright 2017 by the system-query package contributors, Apache License 2.0,
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
