"""Functions to query system's hard drives."""

import itertools
import logging
import typing as t

from .available_features import pyudev, HDD

IGNORED_DEVICE_PATHS = {'/dev/bus', '/dev/dm', '/dev/loop', '/dev/md', '/dev/sr'}

_LOG = logging.getLogger(__name__)


def query_hdds() -> t.Dict[str, dict]:
    """Get information about all hard drives."""
    if not HDD:
        return {}
    context = pyudev.Context()
    hdds = {}
    for device in context.list_devices(subsystem='block', DEVTYPE='disk'):
        if device.device_node is None or any(
                device.device_node.startswith(_) for _ in IGNORED_DEVICE_PATHS):
            continue
        hdd = {'size': device.attributes.asint('size')}
        for device_ in itertools.chain([device], device.ancestors):
            try:
                hdd['model'] = device_.attributes.asstring('model').strip()
            except KeyError:
                _LOG.debug('device %s has no attribute "model"', device_.device_path)
                continue
            else:
                _LOG.debug(
                    'got model "%s" for device %s from device %s',
                    hdd['model'], device.device_path, device_.device_path)
            break
        hdds[device.device_node] = hdd
    return hdds
