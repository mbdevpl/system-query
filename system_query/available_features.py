
import logging

_LOG = logging.getLogger(__name__)

try:
    import cpuinfo
except ImportError:
    cpuinfo = None
    _LOG.info("unable to import package cpuinfo", exc_info=1)
except Exception:
    # raise Exception("py-cpuinfo currently only works on X86 and some ARM CPUs.")
    cpuinfo = None
    _LOG.info("package cpuinfo doesn't work on this system", exc_info=1)

CPU = cpuinfo is not None

try:
    import psutil
except ImportError:
    psutil = None
    _LOG.info("unable to import package psutil", exc_info=1)

CPU_CLOCK = psutil is not None
CPU_CORES = psutil is not None

try:
    import pyudev
    pyudev.Context()
except ImportError:
    pyudev = None
    _LOG.info("unable to import package pyudev", exc_info=1)

HDD = pyudev is not None
