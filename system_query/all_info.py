"""Functions that aggregate results of multiple queries."""

import typing as t

from .cpu_info import query_cpu
from .gpu_info import query_gpus
from .hdd_info import query_hdd
from .host_info import query_host
from .os_info import query_os
from .ram_info import query_ram
from .swap_info import query_swap


def query_all(**kwargs) -> t.Mapping[str, t.Any]:
    return {
        'host': query_host(),
        'os': query_os(),
        # 'software': query_software(),
        'cpu': query_cpu(**kwargs),
        'gpus': query_gpus(**kwargs),
        'ram': query_ram(**kwargs),
        'hdds': query_hdd(),
        'swap': query_swap(),
        # 'network': psutil.net_if_stats()
        }
