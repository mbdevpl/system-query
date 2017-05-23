"""Functions to query GPUs in the system."""

import logging
import typing as t

from .errors import QueryError

_LOG = logging.getLogger(__name__)

try:

    try:
        import pycuda
        import pycuda.driver as cuda
    except ImportError as err:
        raise QueryError('unable to import pycuda') from err

    try:
        import pycuda.autoinit
    except pycuda._driver.Error as err:
        raise QueryError('') from err


    def query_gpus(**_) -> t.List[t.Mapping[str, t.Any]]:
        """Get information about all GPUs."""
        gpus = []
        for i in range(cuda.Device.count()):
            device = cuda.Device(i)
            gpus.append(query_gpu(device))
        return gpus


    def query_gpu(device: 'cuda.Device') -> t.Mapping[str, t.Any]:
        """Get information about a given GPU."""
        attributes = device.get_attributes()
        cuda_version = device.compute_capability()
        multiprocessors = attributes[cuda.device_attribute.MULTIPROCESSOR_COUNT]
        cuda_cores = calculate_cuda_cores(cuda_version, multiprocessors)
        try:
            return {
                'brand': device.name(),
                'memory': device.total_memory(),
                'memory_clock': attributes[cuda.device_attribute.MEMORY_CLOCK_RATE],
                'cuda_version': float('.'.join(str(_) for _ in cuda_version)),
                'clock': attributes[cuda.device_attribute.CLOCK_RATE],
                'multiprocessors': multiprocessors,
                'cores': cuda_cores,
                'warp_size': attributes[cuda.device_attribute.WARP_SIZE]
                }
        except KeyError as err:
            raise QueryError(
                'expected value not present among device attributes: {}'
                .format(device.get_attributes())) from err


except QueryError:

    _LOG.info('proceeding without GPU query support', exc_info=1)


    def query_gpus(**_):
        return []


def calculate_cuda_cores(cuda_version: t.Tuple[int, int], multiprocessors: int) -> int:
    """Calculate number of cuda cores according to Nvidia's specifications."""
    if cuda_version[0] == 2: # Fermi
        if cuda_version[1] == 1:
            return multiprocessors * 48
        return multiprocessors * 32
    elif cuda_version[0] == 3: # Kepler
        return multiprocessors * 192
    elif cuda_version[0] == 5: # Maxwell
        return multiprocessors * 128
    elif cuda_version[0] == 6: # Pascal
        if cuda_version[1] == 0:
            return multiprocessors * 64
        elif cuda_version[1] == 1:
            return multiprocessors * 128
        return None
    return None
