"""Functions to query system's CPUs/APUs."""

import typing as t

import cpuinfo
import psutil


def query_cpu(**_) -> t.Mapping[str, t.Any]:
    """Get information about CPU present in the system."""
    cpu = cpuinfo.get_cpu_info()
    try:
        cpu_clock = psutil.cpu_freq()
    except NotImplementedError:
        cpu_clock = None
    return {
        'brand': cpu["brand"],
        #'count': cpu["count"],
        'logical_cores': psutil.cpu_count(),
        'physical_cores': psutil.cpu_count(logical=False),
        'clock': cpu_clock.current,
        'clock_min': cpu_clock.min,
        'clock_max': cpu_clock.max}
