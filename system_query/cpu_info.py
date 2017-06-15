"""Functions to query system's CPUs/APUs."""

import logging
import typing as t

import cpuinfo

from .errors import QueryError

_LOG = logging.getLogger(__name__)


try:

    try:
        import psutil
    except ImportError as err:
        raise QueryError('unable to import psutil') from err


    def query_cpu_clock() -> t.Tuple[t.Optional[int], t.Optional[int], t.Optional[int]]:
        """Get current, minimum and maximum clock frequency of the CPU in the system."""
        cpu_clock = None
        try:
            cpu_clock = psutil.cpu_freq()
        except FileNotFoundError:
            pass
        if cpu_clock is None:
            return None, None, None
        return cpu_clock.current, cpu_clock.min, cpu_clock.max


    def query_cpu_cores() -> t.Tuple[t.Optional[int], t.Optional[int]]:
        """Get number of logical and physical cores of the system's CPU."""
        return psutil.cpu_count(), psutil.cpu_count(logical=False)


except QueryError:

    _LOG.info('proceeding without CPU clock and core count query support', exc_info=1)


    def query_cpu_clock() -> t.Tuple[t.Optional[int], t.Optional[int], t.Optional[int]]:
        return None, None, None

    def query_cpu_cores() -> t.Tuple[t.Optional[int], t.Optional[int]]:
        return None, None


def query_cpu(**_) -> t.Mapping[str, t.Any]:
    """Get information about CPU present in the system."""
    cpu = cpuinfo.get_cpu_info()
    clock_current, clock_min, clock_max = query_cpu_clock()
    logical_cores, physical_cores = query_cpu_cores()
    return {
        'brand': cpu["brand"],
        'logical_cores': logical_cores,
        'physical_cores': physical_cores,
        'clock': clock_current,
        'clock_min': clock_min,
        'clock_max': clock_max}
