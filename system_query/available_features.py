
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

try:
    import pint
except ImportError:
    pint = None
    _LOG.info("unable to import package pint", exc_info=1)

CPU = cpuinfo is not None and pint is not None

try:
    import psutil
except ImportError:
    psutil = None
    _LOG.info("unable to import package psutil", exc_info=1)

CPU_CLOCK = psutil is not None
CPU_CORES = psutil is not None

try:
    import pycuda
    import pycuda.driver as cuda
    import pycuda.autoinit
    _LOG.debug('using CUDA version %s', '.'.join(str(_) for _ in cuda.get_version()))
except ImportError:
    cuda = None
    _LOG.info("unable to import package pycuda", exc_info=1)
except pycuda._driver.Error:
    cuda = None
    _LOG.info("unable to initialize cuda", exc_info=1)

GPU = cuda is not None

try:
    import pyudev
    pyudev.Context()
except ImportError:
    pyudev = None
    _LOG.info("unable to import package pyudev", exc_info=1)

HDD = pyudev is not None

RAM_TOTAL = psutil is not None

SWAP = psutil is not None
