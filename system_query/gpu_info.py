"""Functions to query GPUs in the system."""

import typing as t

from .available_features import cuda, GPU

from .errors import QueryError


def query_gpus(**_) -> t.List[t.Mapping[str, t.Any]]:
    """Get information about all GPUs."""
    if not GPU:
        return []
    gpus = []
    for i in range(cuda.Device.count()):
        device = cuda.Device(i)
        gpus.append(query_gpu(device))
    return gpus


def query_gpu(device: 'cuda.Device') -> t.Mapping[str, t.Any]:
    """Get information about a given GPU."""
    attributes = device.get_attributes()
    compute_capability = device.compute_capability()
    multiprocessors = attributes[cuda.device_attribute.MULTIPROCESSOR_COUNT]
    cuda_cores = calculate_cuda_cores(compute_capability, multiprocessors)
    try:
        return {
            'brand': device.name(),
            'memory': device.total_memory(),
            'memory_clock': attributes[cuda.device_attribute.MEMORY_CLOCK_RATE],
            'compute_capability': float('.'.join(str(_) for _ in compute_capability)),
            'clock': attributes[cuda.device_attribute.CLOCK_RATE],
            'multiprocessors': multiprocessors,
            'cores': cuda_cores,
            'warp_size': attributes[cuda.device_attribute.WARP_SIZE]
            }
    except KeyError as err:
        raise QueryError(
            'expected value not present among device attributes: {}'
            .format(device.get_attributes())) from err


def calculate_cuda_cores(compute_capability: t.Tuple[int, int], multiprocessors: int) -> int:
    """Calculate number of cuda cores according to Nvidia's specifications."""
    if compute_capability[0] == 2:  # Fermi
        if compute_capability[1] == 1:
            return multiprocessors * 48
        return multiprocessors * 32
    if compute_capability[0] == 3:  # Kepler
        return multiprocessors * 192
    if compute_capability[0] == 5:  # Maxwell
        return multiprocessors * 128
    if compute_capability[0] == 6:  # Pascal
        if compute_capability[1] == 0:
            return multiprocessors * 64
        if compute_capability[1] == 1:
            return multiprocessors * 128
    return None
