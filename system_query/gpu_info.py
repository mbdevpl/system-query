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
            f'expected value not present among device attributes: {device.get_attributes()}'
            ) from err


COMPUTE_CAPABILITY_MULTIPLIERS = {
    # Fermi
    2: {1: 48, None: 32},
    # Kepler
    3: 192,
    # Maxwell
    5: 128,
    # Pascal
    6: {0: 64, 1: 128}
}


def calculate_cuda_cores(compute_capability: t.Tuple[int, int],
                         multiprocessors: int) -> t.Optional[int]:
    """Calculate number of cuda cores according to Nvidia's specifications.

    Source: https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#compute-capabilities
    """
    multiplier_major = COMPUTE_CAPABILITY_MULTIPLIERS.get(compute_capability[0])
    if isinstance(multiplier_major, int):
        return multiprocessors * multiplier_major
    if isinstance(multiplier_major, dict):
        multiplier_minor = multiplier_major.get(compute_capability[1])
        if multiplier_minor is None and None in multiplier_major:
            multiplier_minor = multiplier_major[None]
        if multiplier_minor is None:
            return None
        return multiprocessors * multiplier_minor
    return None
