"""Functions to query the host."""

import platform


def query_host() -> str:
    hostname = platform.node()
    return hostname
