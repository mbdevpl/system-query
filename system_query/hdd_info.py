"""Functions to query system's hard drives."""

import itertools
import logging
import typing as t

import pyudev

from .errors import QueryError

_LOG = logging.getLogger(__name__)


def query_hdd() -> t.Dict[str, dict]:
    context = pyudev.Context()
    hdds = {}
    for device in context.list_devices(subsystem='block', DEVTYPE='disk'):
        if 'loop' in device.device_path or 'md' in device.device_path:
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


try:

    # try:
    #     import psutil
    # except ImportError as err:
    #     raise QueryError('unable to import psutil') from err

    def _query_hdd_old() -> t.Dict[str, dict]:
        import fcntl
        import glob
        import os
        import struct
        # import sys

        def list_devices(pattern: str = 'sd*'):
            return [os.path.basename(d) for d in glob.glob('/sys/block/' + pattern)]

        # https://stackoverflow.com/questions/4193514/get-hard-disk-serial-number-using-python-on-linux
        def get_identity(dev):

            fields = ()
            try:
                with open('/dev/' + dev, "rb") as fd:

                    hd_driveid_format_str = "@ 10H 20s 3H 8s 40s 2B H 2B H 4B 6H 2B I 36H I Q 152H"
                    HDIO_GET_IDENTITY = 0x030d
                    sizeof_hd_driveid = struct.calcsize(hd_driveid_format_str)
                    assert sizeof_hd_driveid == 512

                    buf = fcntl.ioctl(fd, HDIO_GET_IDENTITY, " " * sizeof_hd_driveid)
                    fields = struct.unpack(hd_driveid_format_str, buf)
                    return (dev, fields[15].strip(), fields[10].strip(), fields[14].strip())

            except IOError:
                raise

            return fields

        # if os.geteuid() > 0:
        #    print("ERROR: Must be run as root")
        #    sys.exit(1)

        devices = list_devices()
        if devices:
            fmt = "{0:<6}  {1:<40}  {2:<20}  {3:<8}"
            print(fmt.format('Device', 'Model', 'Serial', 'Firmware'))
            print('-' * 80)
            for device in devices:
                identity = get_identity(device)
                if identity:
                    print(fmt.format(*identity))
        else:
            print("No devices found.")

        # total_swap = psutil.swap_memory().total
        # return total_swap


except QueryError:

    _LOG.info('proceeding without swap query support', exc_info=1)

    def _query_hdd() -> t.Optional[int]:
        return None
