"""Probe the system for available features to estalbish what can be queried."""

import logging

_LOG = logging.getLogger(__name__)

try:
    import cpuinfo
except ImportError:
    cpuinfo = None
    _LOG.info("unable to import package cpuinfo", exc_info=True)
except:  # pylint: disable = bare-except  # noqa: E722
    # raise Exception("py-cpuinfo currently only works on X86 and some ARM CPUs.")
    cpuinfo = None  # pylint: disable = invalid-name
    _LOG.info("package cpuinfo doesn't work on this system", exc_info=True)

try:
    import pint
except ImportError:
    pint = None
    _LOG.info("unable to import package pint", exc_info=True)

CPU = cpuinfo is not None and pint is not None

try:
    import psutil
except ImportError:
    psutil = None
    _LOG.info("unable to import package psutil", exc_info=True)

CPU_CLOCK = psutil is not None
CPU_CORES = psutil is not None

_cuda_failed = False
try:
    import pycuda
except ImportError:
    _cuda_failed = True
    _LOG.info("unable to import package pycuda", exc_info=True)
else:
    try:
        import pycuda.driver as cuda
    except ImportError:
        _cuda_failed = True
        _LOG.info("unable to import package pycuda.driver", exc_info=True)
    else:
        try:
            import pycuda.autoinit
        except pycuda._driver.Error:  # pylint: disable = protected-access
            _cuda_failed = True
            _LOG.info("unable to initialize cuda", exc_info=True)
        else:
            _LOG.debug('using CUDA version %s', '.'.join(str(_) for _ in cuda.get_version()))

if _cuda_failed:
    cuda = None  # pylint: disable = invalid-name

GPU = cuda is not None

try:
    import pyudev
except ImportError:
    pyudev = None
    _LOG.info("unable to import package pyudev", exc_info=True)
else:
    pyudev.Context()

HDD = pyudev is not None

RAM_TOTAL = psutil is not None

SWAP = psutil is not None
