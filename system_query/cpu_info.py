"""Functions to query system's CPUs/APUs."""

import typing as t

import cpuinfo
import psutil


def query_cpu(**_) -> t.Mapping[str, t.Any]:
    """Get information about CPU present in the system."""
    cpu = cpuinfo.get_cpu_info()
    try:
        cpu_clock = psutil.cpu_freq()
        clock_current = cpu_clock.current
        clock_min = cpu_clock.min
        clock_max = cpu_clock.max
    except FileNotFoundError:
        clock_current = None
        clock_min = None
        clock_max = None
    return {
        'brand': cpu["brand"],
        'logical_cores': psutil.cpu_count(),
        'physical_cores': psutil.cpu_count(logical=False),
        'clock': clock_current,
        'clock_min': clock_min,
        'clock_max': clock_max}
