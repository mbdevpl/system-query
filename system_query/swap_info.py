"""Functions to query system's swap memory."""

import typing as t

from .available_features import psutil, SWAP


def query_swap(**_) -> t.Optional[t.Dict[str, t.Any]]:
    """Get information about swap."""
    if not SWAP:
        return None
    total_swap = psutil.swap_memory().total
    return {'total': total_swap}
