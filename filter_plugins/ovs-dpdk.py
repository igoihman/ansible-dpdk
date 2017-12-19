from __future__ import (absolute_import, division, print_function)


def get_core_mask(cores):
    mask = 0
    for core in cores:
        mask |= (1 << int(core))
    return hex(mask)
