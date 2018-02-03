"""Query and export system data in one step."""

import json
import pathlib
import pprint
import sys
import typing as t

from .all_info import query_all
from .cpu_info import query_cpu
from .gpu_info import query_gpus
from .ram_info import query_ram

JSON_INDENT = 2

JSON_ENSURE_ASCII = False


def query_and_export(query_scope: str, export_format: str, export_target: t.Any, **kwargs):
    """Query the given scope of the system and export results in a given format to a given target.

    Currently implemented values are:

    - query_scope: all, cpu, gpu, ram.
    - export_format: json, raw.
    - export_target: sys.stdout, sys.stderr, path.
    """

    info = query(query_scope, **kwargs)
    export(info, export_format, export_target)


def query(query_scope: str, **kwargs):
    """Wrapper around selected system query functions."""
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
    return info


def export(info, export_format: str, export_target: t.Any):
    """Export information obtained by system query to a specified format."""
    if export_format == 'json':
        if export_target in (sys.stdout, sys.stderr):
            json_str = json.dumps(info, indent=JSON_INDENT, ensure_ascii=JSON_ENSURE_ASCII)
            print(json_str, file=export_target)
        elif isinstance(export_target, pathlib.Path):
            with open(str(export_target), 'w', encoding='utf-8') as json_file:
                json.dump(info, json_file, indent=JSON_INDENT, ensure_ascii=JSON_ENSURE_ASCII)
        else:
            raise NotImplementedError('format={} target={}'.format(export_format, export_target))
    elif export_format == 'raw':
        if export_target in (sys.stdout, sys.stderr):
            pprint.pprint(info, stream=export_target)
        elif isinstance(export_target, pathlib.Path):
            with open(str(export_target), 'a', encoding='utf-8') as text_file:
                text_file.write(str(info))
        else:
            raise NotImplementedError('format={} target={}'.format(export_format, export_target))
    else:
        raise NotImplementedError('format={} target={}'.format(export_format, export_target))
