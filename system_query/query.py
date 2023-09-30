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
from .swap_info import query_swap

JSON_INDENT = 2

JSON_ENSURE_ASCII = False


def query_and_export(query_scope: str, export_format: str, export_target: t.Any, **kwargs):
    """Query the given scope of the system and export results in a given format to a given target.

    Currently implemented values are:

    - query_scope: all, cpu, gpu, ram, swap.
    - export_format: json, raw.
    - export_target: sys.stdout, sys.stderr, path.
    """
    info = query(query_scope, **kwargs)
    export(info, export_format, export_target)


QUERY_FUNCTIONS = {
    'all': query_all,
    'cpu': query_cpu,
    'gpu': query_gpus,
    'ram': query_ram,
    'swap': query_swap,
}


def query(query_scope: str, **kwargs) -> t.Any:
    """Wrap around selected system query functions."""
    try:
        query_function = QUERY_FUNCTIONS[query_scope]
    except KeyError as err:
        raise NotImplementedError(f'scope={query_scope}') from err
    return query_function(**kwargs)  # type: ignore


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
            raise NotImplementedError(f'format={export_format} target={export_target}')
    elif export_format == 'raw':
        if export_target in (sys.stdout, sys.stderr):
            pprint.pprint(info, stream=export_target)
        elif isinstance(export_target, pathlib.Path):
            with open(str(export_target), 'a', encoding='utf-8') as text_file:
                text_file.write(str(info))
        else:
            raise NotImplementedError(f'format={export_format} target={export_target}')
    else:
        raise NotImplementedError(f'format={export_format} target={export_target}')
