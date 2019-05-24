"""This is __init__ module of system_query package."""

from ._version import VERSION
from .all_info import query_all
from .cpu_info import query_cpu
from .gpu_info import query_gpus
# from .host_info import query_host
# from .os_info import query_os
from .ram_info import query_ram
from .software_info import query_software
# from .swap_info import query_swap
from .query import query_and_export

__version__ = VERSION

__all__ = [
    'query_all', 'query_cpu', 'query_gpus', 'query_ram', 'query_software', 'query_and_export']
