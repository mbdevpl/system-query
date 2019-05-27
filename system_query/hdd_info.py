"""Functions to query system's hard drives."""

import itertools
# import logging
import typing as t

from .available_features import pyudev, HDD

# _LOG = logging.getLogger(__name__)

IGNORED_DEVICE_PATHS = {'/dm', '/loop', '/md'}


def query_hdd() -> t.Dict[str, dict]:
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
                break
            except KeyError:
                pass
        hdds[device.device_node] = hdd
    return hdds
