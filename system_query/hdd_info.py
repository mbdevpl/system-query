"""Functions to query system's hard drives."""

import itertools
import logging
import typing as t

from .errors import QueryError

_LOG = logging.getLogger(__name__)

IGNORED_DEVICE_PATHS = {'/dm', '/loop', '/md'}


try:

    try:
        import pyudev
        pyudev.Context()
    except ImportError as err:
        raise QueryError('unable to import pyudev') from err

    def query_hdd() -> t.Dict[str, dict]:
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

except QueryError:

    _LOG.info('proceeding without hdd query support', exc_info=1)

    def query_hdd() -> t.Dict[str, dict]:
        return {}
