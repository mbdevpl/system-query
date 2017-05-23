"""Functions to query system's swap memory."""

import psutil

def query_swap() -> int:
    total_swap = psutil.swap_memory().total
    return total_swap
