"""Functions to query system's RAM."""

import logging
import subprocess
import typing as t
from xml.etree import ElementTree as ET

import psutil

_LOG = logging.getLogger(__name__)


def query_ram(sudo: bool = False, **kwargs) -> t.Mapping[str, t.Any]:
    total_ram = psutil.virtual_memory().total
    ram_banks = query_ram_banks(sudo=sudo, **kwargs)
    return {
        'total': total_ram,
        'banks': ram_banks}


def query_ram_banks(sudo: bool = False, **_) -> t.List[t.Mapping[str, t.Any]]:
    """Extract information about RAM dice installed in the system."""
    try:
        xml_root = parse_lshw(sudo=sudo)
    except FileNotFoundError:
        return []
    nodes = xml_root.findall('.//node')
    _LOG.debug('%i nodes', len(nodes))
    ram_banks = []
    for node in nodes:
        node_id = node.attrib['id']
        _LOG.debug('%s', node_id)
        if not node_id.startswith('bank'):
            continue
        ram_banks.append(query_ram_bank(node))
    return ram_banks


def parse_lshw(sudo: bool = False):
    cmd = (['sudo'] if sudo else []) + ['lshw', '-xml', '-quiet']
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ET.fromstring(result.stdout.decode())


def query_ram_bank(node: ET.Element) -> t.Mapping[str, t.Any]:
    """Extract information about given RAM bank from XML node."""
    bank_size = node.findall('./size')
    bank_clock = node.findall('./clock')
    if len(bank_size) != 1 or len(bank_clock) != 1:
        _LOG.warning(
            'there should be exactly one size and clock value for a bank'\
            ' but there are %i and %i respectively', len(bank_size), len(bank_clock))
    _LOG.debug(ET.tostring(node, encoding='utf8', method='xml').decode())
    return {
        'memory': int(bank_size[0].text),
        'clock': int(bank_clock[0].text)}
