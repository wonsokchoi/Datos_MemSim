import os
import numpy as np
import cache as cc
# import workload_analyzer as wkan
import settings as st
import sys

if __name__ == "__main__":

    conf = st.Settings()
    # Cache settings
    unit = 1 << 13  # 8KB page
    # unit = 1 << 6   # 64B line
    # slots = int(len(footprint)*0.1)
    # slots = 1 << 10    # 16MB
    capacity = 1 << 21 # 2MB
    # slots = 1 << 8    # 2MB / 8 proceses / 256 slots
    # slots = sys.maxsize
    slots = capacity / unit
    # cache = cc.LRUCache(slots, unit)
    cache = cc.OPTCache(slots, unit)
    cache.do_sim(conf)