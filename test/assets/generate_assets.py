#!/usr/bin/env python3

"""Prepare new test assets based on the current system.

This script depends on system_query package to determine what can actually be queried,
and thus what new test assets can be obtained.
"""

import datetime
import json
import logging
import pathlib
import pprint
import sys
import typing as t

import boilerplates.logging

_HERE = pathlib.Path(__file__).resolve().parent
_LOG = logging.getLogger(pathlib.Path(__file__).stem if __name__ == '__main__' else __name__)


class Logging(boilerplates.logging.Logging):
    """Logging configuration."""

    packages = ['generate_assets', 'system_query']


def prepare_test_assets():
    """Prepare new test assets based on the current system."""
    import system_query  # pylint: disable = import-outside-toplevel, import-error
    hostname = system_query.host_info.query_host()
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    if system_query.available_features.CPU:
        prepare_cpu_test_data(_HERE / f'{hostname}_{timestamp}_cpu_data.json')
    if system_query.available_features.GPU:
        prepare_gpu_test_data(_HERE / f'{hostname}_{timestamp}_gpu{{suffix}}_data.json')
    if system_query.available_features.HDD:
        prepare_hdd_test_data(_HERE / f'{hostname}_{timestamp}_hdd_data.json')


def persist_dict(dict_data: dict, filepath: pathlib.Path):
    """Persist a dictionary to a JSON file."""
    _LOG.info('storing data in "%s"', filepath)
    with filepath.open('w', encoding='utf-8') as json_file:
        json.dump(dict_data, json_file, indent=2, ensure_ascii=False)


def make_value_json_serializable(value: t.Any):
    """Force a value to be serializable to JSON."""
    if isinstance(value, bytes):
        try:
            return value.decode()
        except UnicodeDecodeError:
            _LOG.debug('failed to decode value %s to string', value)
        return value.hex()
    return value


def prepare_cpu_test_data(filepath: pathlib.Path):
    """Prepare CPU test data based on the current system."""
    import cpuinfo  # pylint: disable = import-outside-toplevel
    cpuinfo_dict = cpuinfo.get_cpu_info()
    persist_dict(cpuinfo_dict, filepath)


GPU_DATA_PREFIX = '''import pycuda

DATA = '''


def prepare_gpu_test_data(filepath: pathlib.Path):
    """Prepare GPU test data based on the current system."""
    import pycuda.driver as cuda  # pylint: disable = import-outside-toplevel
    import pycuda.autoinit  # pylint: disable = import-outside-toplevel, unused-import  # noqa: F401
    cuda_device_dict = {}
    for i in range(cuda.Device.count()):
        cuda_device = cuda.Device(i)
        cuda_device_dict[i] = str(cuda_device.name())
        cuda_device_str = pprint.pformat(cuda_device.get_attributes(), indent=2, compact=False)
        _LOG.info('storing data in "%s"', filepath)
        with filepath.with_name(filepath.name.format(suffix=f'_{i}')).with_suffix('.py').open(
                'w', encoding='utf-8') as cuda_device_file:
            print(GPU_DATA_PREFIX, end='', file=cuda_device_file)
            print(cuda_device_str, file=cuda_device_file)
    persist_dict(cuda_device_dict, filepath.with_name(filepath.name.format(suffix='')))


def _get_all_hdd_device_attributes(device):
    device_dict = {}
    for attr in device.attributes.available_attributes:
        try:
            device_dict[attr] = device.attributes.asint(attr)
        except KeyError:
            pass
        except ValueError:
            pass
        else:
            continue
        try:
            device_dict[attr] = device.attributes.asstring(attr)
        except KeyError:
            pass
        except UnicodeDecodeError:
            pass
        device_dict[attr] = make_value_json_serializable(device.attributes.get(attr))
    return device_dict


def prepare_hdd_test_data(filepath: pathlib.Path):
    """Prepare HDD test data based on the current system."""
    _LOG.info('generating assets for HDD tests')
    import pyudev  # pylint: disable = import-outside-toplevel
    from system_query.hdd_info import \
        IGNORED_DEVICE_PATHS  # pylint: disable = import-outside-toplevel, import-error
    context = pyudev.Context()
    pyudev_devices_dict = {}
    for device in context.list_devices(subsystem='block', DEVTYPE='disk'):
        pyudev_device_dict = {}
        if device.device_node is None or any(
                device.device_node.startswith(_) for _ in IGNORED_DEVICE_PATHS):
            continue
        pyudev_device_dict[device.device_path] = _get_all_hdd_device_attributes(device)
        for dev in device.ancestors:
            if dev.device_node is not None and any(
                    dev.device_node.startswith(_) for _ in IGNORED_DEVICE_PATHS):
                continue
            pyudev_device_dict[dev.device_path] = _get_all_hdd_device_attributes(dev)
        pyudev_devices_dict[device.device_node] = pyudev_device_dict
    persist_dict(pyudev_devices_dict, filepath)


if __name__ == '__main__':
    sys.path.insert(0, str(_HERE.parent.parent))
    Logging.configure()
    prepare_test_assets()
