"""Functions to query system's hard drives."""

import itertools
import typing as t

from .available_features import pyudev, HDD

IGNORED_DEVICE_PATHS = {'/dm', '/loop', '/md'}


def query_hdds() -> t.Dict[str, dict]:
    """Get information about all hard drives."""
    if not HDD:
        return {}
    context = pyudev.Context()
    hdds = {}
    for device in context.list_devices(subsystem='block', DEVTYPE='disk'):
        if any(_ in device.device_path for _ in IGNORED_DEVICE_PATHS):
            continue
        hdd = {'size': device.attributes.asint('size')}
        for device_ in itertools.chain([device], device.ancestors):
            try:
                hdd['model'] = device_.attributes.asstring('model')
            except KeyError:
                continue
            break
        hdds[device.device_node] = hdd
    return hdds
