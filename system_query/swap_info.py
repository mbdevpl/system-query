"""Functions to query system's swap memory."""

import logging
import typing as t

from .errors import QueryError

_LOG = logging.getLogger(__name__)


try:

    try:
        import psutil
    except ImportError as err:
        raise QueryError('unable to import psutil') from err

    def query_swap() -> t.Optional[int]:
        total_swap = psutil.swap_memory().total
        return total_swap


except QueryError:

    _LOG.info('proceeding without swap query support', exc_info=1)

    def query_swap() -> t.Optional[int]:
        return None
